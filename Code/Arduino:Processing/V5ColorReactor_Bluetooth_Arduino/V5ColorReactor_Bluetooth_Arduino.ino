/*
  ESP32 Bluetooth Classic + Button + Non-blocking GPIO scheduler
  Controls multi-wavelength LED reactor via Bluetooth position commands + physical button
  Faithful port of pote_espLights_noBlock.ino (potentiometer version)

  Input methods:
    - Bluetooth: "MOVE <0-6>" to move immediately, "BLEACH" for swatch reset, "STATUS", "STOP", "DEBUG ON/OFF"
    - Physical button (pin 32): press to execute move to target position (bleach when at pos 0 with target 0)
    - USB Serial: same commands as Bluetooth (for bench testing)

  App swatch layout (top to bottom):
    - Swatch Reset (sends BLEACH) — white box with em dash, bleaches to baseline
    - Level 10 (pos 0) through Level 4 (pos 6) — color swatches, send MOVE <pos>

  Down-movement logic (EXACT match to original):
    1. Always bleach fully to position 0 (sum backwardTimes[fromPosition] down to backwardTimes[1])
    2. Then recharge from 0 to target using UV (sum forwardTimes[0] to forwardTimes[target-1])
*/

#include "BluetoothSerial.h"
#include <map>
#include <vector>
#include <algorithm>
#include <cstring>
#include <freertos/FreeRTOS.h>
#include <freertos/queue.h>

// Forward declaration for Arduino IDE prototype generation
struct Command;

// ===== Timing arrays for position transitions (in milliseconds) =====

// CHARGING TIMES: UV light exposure (265nm + 367nm) for each step UP
// Index i = time needed to move from position i to position i+1
static uint32_t forwardTimes[7] = {
  500,    // 0->1: 0.5 seconds
  800,    // 1->2: 0.8 seconds
  1400,   // 2->3: 1.4 seconds
  2100,   // 3->4: 2.1 seconds
  3000,   // 4->5: 3 seconds
  4000,   // 5->6: 4 seconds
  5000    // 6->7: 5 seconds
};

// BLEACHING TIMES: Visible light exposure for each step DOWN (used during RESET)
// Index i = time needed to bleach from position i to position i-1
static uint32_t backwardTimes[7] = {
  2000,   // 1->0: 2 seconds
  3000,   // 2->1: 3 seconds
  3000,   // 3->2: 3 seconds
  3000,   // 4->3: 3 seconds
  3000,   // 5->4: 3 seconds
  3000,   // 6->5: 3 seconds
  5000    // 7->6: 5 seconds
};

// MANUAL BLEACH TIME
static const uint32_t MANUAL_BLEACH_TIME = 5000;  // 5 seconds

// UV BASE CHARGE after swatch reset — Level 10 needs this to go from "reset" to actual Level 10
static const uint32_t RESET_BASE_UV_TIME = 500;   // 500ms

bool debug = false;

// ===== Bluetooth setup =====
BluetoothSerial SerialBT;
const String DEVICE_NAME = "ColorReactor";
static bool btConnected = false;
static bool btDebug = true;  // Bluetooth-specific debug messages

// ===== Hardware pins =====
static const int BUTTON_PIN = 32;   // Button with pull-up (other side to 3V3)
static const int ONBOARD_LED = 2;   // Onboard LED (blinks during UV exposure)

// ===== Your available LED pins =====
static int ALL_PINS[] = { 4, 5, 13, 14, 23, 25, 26, 27 };
static const size_t ALL_PINS_LEN = sizeof(ALL_PINS) / sizeof(ALL_PINS[0]);

// ===== Position state tracking =====
static int currentPosition = 0;
static int targetPosition = 0;   // Set by Bluetooth POS command (replaces potentiometer)
static bool swatchIsReset = false; // True after manual bleach — next MOVE always executes

// ===== Label -> pin defaults (same map structure as original) =====
std::map<String, int> labelToPin = {
  { "265nm", 25 },
  { "367nm", 26 },
  { "450nm", 14 },
  { "425nm", 27 },
  { "522nm", 13 },
  { "632nm", 4 },
  { "657nm", 5 },
  { "727nm", 23 },
};

// ===== Serial output helper (sends to both USB + BT) =====
static inline void txNotify(const String& msg) {
  Serial.println(msg);
  if (SerialBT.hasClient()) {
    SerialBT.println(msg);
  }
}

// Bluetooth-only debug (only when btDebug is on)
static inline void btLog(const String& msg) {
  if (!btDebug) return;
  String out = "< BT_DEBUG: " + msg;
  Serial.println(out);
  if (SerialBT.hasClient()) {
    SerialBT.println(out);
  }
}

// ===== Utilities (same as original) =====
static inline String trimStr(const String& s) {
  String t = s;
  t.trim();
  return t;
}
static inline String upperStr(const String& s) {
  String t = s;
  t.toUpperCase();
  return t;
}
static inline std::vector<String> splitWS(const String& s) {
  std::vector<String> parts;
  int i = 0, n = s.length();
  while (i < n) {
    while (i < n && isspace((unsigned char)s[i])) i++;
    if (i >= n) break;
    int j = i;
    while (j < n && !isspace((unsigned char)s[j])) j++;
    parts.push_back(s.substring(i, j));
    i = j;
  }
  return parts;
}

static inline void safePinModeOutput(int pin) {
  pinMode(pin, OUTPUT);
}
static inline void setPinLevel(int pin, bool high) {
  safePinModeOutput(pin);
  digitalWrite(pin, high ? HIGH : LOW);
}
static inline void allOff() {
  for (size_t i = 0; i < ALL_PINS_LEN; ++i) {
    safePinModeOutput(ALL_PINS[i]);
    digitalWrite(ALL_PINS[i], LOW);
  }
}

// ===== Non-blocking pulse tracking (same as original) =====
struct Pulse {
  int pin;
  uint32_t offAt;
};
std::vector<Pulse> activePulses;

static void schedulePulse(int pin, uint32_t durationMs) {
  const uint32_t now = millis();
  const uint32_t offAt = now + durationMs;
  for (auto& p : activePulses) {
    if (p.pin == pin) {
      if ((int32_t)(offAt - p.offAt) > 0) p.offAt = offAt;
      setPinLevel(pin, true);
      return;
    }
  }
  setPinLevel(pin, true);
  activePulses.push_back({ pin, offAt });
}

static void servicePulses() {
  const uint32_t now = millis();
  activePulses.erase(
    std::remove_if(activePulses.begin(), activePulses.end(),
                   [&](const Pulse& p) {
                     if ((int32_t)(now - p.offAt) >= 0) {
                       setPinLevel(p.pin, false);
                       return true;
                     }
                     return false;
                   }),
    activePulses.end());
}

// Resolve label -> pin (same as original)
static bool resolveLabelPin(const String& label, int& pinOut) {
  auto it = labelToPin.find(label);
  if (it == labelToPin.end()) return false;
  pinOut = it->second;
  return true;
}

// ===== Button handling (exact copy from original) =====
static bool lastStableButtonState = LOW;
static bool lastRawReading = LOW;
static uint32_t lastDebounceTime = 0;
static const uint32_t DEBOUNCE_DELAY = 50;

static bool buttonPressed() {
  bool reading = digitalRead(BUTTON_PIN);

  if (reading != lastRawReading) {
    lastDebounceTime = millis();
    lastRawReading = reading;
    txNotify("< BTN DEBUG: Raw state change detected! reading=" + String(reading));
  }

  bool pressed = false;
  uint32_t timeSinceChange = millis() - lastDebounceTime;

  if (timeSinceChange > DEBOUNCE_DELAY) {
    if (reading == HIGH && lastStableButtonState == LOW) {
      txNotify("< BTN DEBUG: RISING EDGE! Registering press");
      pressed = true;
      lastStableButtonState = HIGH;
    } else if (reading == LOW && lastStableButtonState == HIGH) {
      txNotify("< BTN DEBUG: FALLING EDGE");
      lastStableButtonState = LOW;
    }
  }

  return pressed;
}

// ===== Debug logging =====
static void logDebugInfo() {
  static uint32_t lastDebugLog = 0;
  if (millis() - lastDebugLog > 500) {
    int btnReading = digitalRead(BUTTON_PIN);
    txNotify("< DEBUG: Button=" + String(btnReading) +
             ", stable=" + String(lastStableButtonState) +
             ", current=" + String(currentPosition) +
             ", target=" + String(targetPosition) +
             ", btConn=" + String(SerialBT.hasClient() ? "YES" : "NO"));
    lastDebugLog = millis();
  }
}

// ===== Onboard LED blinking (non-blocking, same as original) =====
static bool uvLightsActive = false;
static uint32_t lastBlinkTime = 0;
static bool blinkState = false;
static const uint32_t BLINK_INTERVAL = 100;

static void updateBlinkingLED() {
  if (uvLightsActive) {
    if (millis() - lastBlinkTime >= BLINK_INTERVAL) {
      blinkState = !blinkState;
      digitalWrite(ONBOARD_LED, blinkState ? HIGH : LOW);
      lastBlinkTime = millis();
    }
  } else {
    digitalWrite(ONBOARD_LED, LOW);
    blinkState = false;
  }
}

// ===== Non-blocking delay with LED blinking (same as original) =====
static void delayWithBlink(uint32_t durationMs) {
  uint32_t startTime = millis();
  while ((millis() - startTime) < durationMs) {
    updateBlinkingLED();
    delay(1);
  }
}

// ===== Position handshake: always tell the app where we are =====
static void sendPositionUpdate() {
  txNotify("< POS_UPDATE:" + String(currentPosition));
}

// ===== Move function (EXACT logic from original pote_espLights_noBlock.ino) =====
static void moveTo(int fromPosition, int toPosition) {
  if (fromPosition == toPosition) {
    txNotify("< INFO: Already at position " + String(fromPosition));
    return;
  }

  txNotify("< MOVE START: " + String(fromPosition) + " -> " + String(toPosition));

  bool movingForward = (toPosition > fromPosition);

  if (movingForward) {
    // Moving UP (e.g., 2->5): Simply add UV light
    uint32_t totalTime = 0;
    for (int i = fromPosition; i < toPosition; i++) {
      totalTime += forwardTimes[i];
    }

    txNotify("< CHARGING UP: UV lights ON for " + String(totalTime) + "ms");

    // Turn on UV lights (using resolveLabelPin, same as original)
    int pin265, pin367;
    if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, true);
    if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, true);

    uvLightsActive = true;
    delayWithBlink(totalTime);
    uvLightsActive = false;

    // Turn off UV lights
    if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, false);
    if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, false);

  } else {
    // ================================================================
    // Moving DOWN (e.g., 5->2): RESET to 0, then charge to target
    // THIS IS THE CRITICAL SECTION - exact match to original logic
    // ================================================================

    // Step 1: Calculate bleaching time - ALWAYS bleach all the way to position 0
    // Original loop: for (int i = fromPosition; i > 0; i--) bleachTime += backwardTimes[i];
    uint32_t bleachTime = 0;
    for (int i = fromPosition; i > 0; i--) {
      bleachTime += backwardTimes[i];
    }

    txNotify("< RESET: Bleaching to position 0 with visible lights for " + String(bleachTime) + "ms");

    // Turn on all visible lights (450nm, 425nm, 522nm, 632nm, 657nm, 727nm)
    const char* visibleLabels[] = {"450nm", "425nm", "522nm", "632nm", "657nm", "727nm"};
    int visiblePins[6];
    int visiblePinCount = 0;

    for (int i = 0; i < 6; i++) {
      int pin;
      if (resolveLabelPin(visibleLabels[i], pin)) {
        visiblePins[visiblePinCount++] = pin;
        setPinLevel(pin, true);
      }
    }

    // Blocking delay for reset (same as original)
    delay(bleachTime);

    // Turn off all visible lights
    for (int i = 0; i < visiblePinCount; i++) {
      setPinLevel(visiblePins[i], false);
    }

    txNotify("< RESET COMPLETE: Now at position 0");

    // Step 2: Charge from 0 to target position using UV
    // For Level 10 (pos 0): use RESET_BASE_UV_TIME since bleach leaves swatch below Level 10
    // For Levels 9-4 (pos 1-6): use existing forwardTimes
    uint32_t chargeTime = (toPosition == 0) ? RESET_BASE_UV_TIME : 0;
    for (int i = 0; i < toPosition; i++) {
      chargeTime += forwardTimes[i];
    }

    if (chargeTime > 0) {
      txNotify("< CHARGING: UV lights ON for " + String(chargeTime) + "ms (0 -> " + String(toPosition) + ")");

      int pin265, pin367;
      if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, true);
      if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, true);

      uvLightsActive = true;
      delayWithBlink(chargeTime);
      uvLightsActive = false;

      if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, false);
      if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, false);
    }
  }

  // Update position and report
  currentPosition = toPosition;
  txNotify("< MOVE COMPLETE: Now at position " + String(toPosition));
  sendPositionUpdate();
}

// ===== Manual bleach: 5 cycles of visible light, then reset position to 0 =====
static const int BLEACH_CYCLES = 5;

static void manualBleach() {
  uint32_t totalTime = MANUAL_BLEACH_TIME * BLEACH_CYCLES;
  txNotify("< MANUAL BLEACH: " + String(BLEACH_CYCLES) + " cycles x " +
           String(MANUAL_BLEACH_TIME) + "ms = " + String(totalTime) + "ms total");
  txNotify("< MANUAL BLEACH: Previous position was " + String(currentPosition));

  // Resolve visible light pins
  const char* visibleLabels[] = {"450nm", "425nm", "522nm", "632nm", "657nm", "727nm"};
  int visiblePins[6];
  int visiblePinCount = 0;

  for (int i = 0; i < 6; i++) {
    int pin;
    if (resolveLabelPin(visibleLabels[i], pin)) {
      visiblePins[visiblePinCount++] = pin;
    }
  }

  for (int cycle = 1; cycle <= BLEACH_CYCLES; cycle++) {
    txNotify("< BLEACH CYCLE " + String(cycle) + "/" + String(BLEACH_CYCLES));

    // Turn on all visible lights
    for (int i = 0; i < visiblePinCount; i++) {
      setPinLevel(visiblePins[i], true);
    }

    delay(MANUAL_BLEACH_TIME);

    // Turn off all visible lights
    for (int i = 0; i < visiblePinCount; i++) {
      setPinLevel(visiblePins[i], false);
    }
  }

  // Reset position tracking to 0 (dye is fully cleared)
  currentPosition = 0;
  targetPosition = 0;
  swatchIsReset = true;  // Next MOVE command always executes (even MOVE 0)

  txNotify("< MANUAL BLEACH COMPLETE: Position reset to 0");
  // Note: Do NOT send sendPositionUpdate() here.
  // POS_UPDATE:0 is ambiguous (Level 10 vs Swatch Reset) and the
  // MANUAL BLEACH COMPLETE message already tells the app to reset state.
}

// ===== Command queue types (same as original) =====
enum CmdType : uint8_t { CMD_NONE = 0,
                         CMD_LED_ON,
                         CMD_GPIO_SET,
                         CMD_ALL_OFF,
                         CMD_MAP,
                         CMD_STOP };

struct Command {
  CmdType type;
  int pin;
  bool level;
  uint32_t duration;
  char label[12];
  int mapPin;
};

QueueHandle_t gCmdQueue = nullptr;

// ===== Bluetooth connection callback =====
void btCallback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
  switch (event) {
    case ESP_SPP_SRV_OPEN_EVT:
      btConnected = true;
      Serial.println("< BT_DEBUG: Client connected!");
      break;
    case ESP_SPP_CLOSE_EVT:
      btConnected = false;
      Serial.println("< BT_DEBUG: Client disconnected");
      break;
    default:
      break;
  }
}

// ===== Command parser (handles both BT and serial, keeps original serial commands too) =====
static void parseCommand(const String& lineIn, const String& source) {
  String line = trimStr(lineIn);
  String U = upperStr(line);

  btLog("RX from " + source + ": [" + line + "]");

  // --- Position command (Bluetooth-style): "POS 3" ---
  if (U.startsWith("POS ")) {
    String posStr = trimStr(line.substring(4));
    int pos = posStr.toInt();

    if (pos < 0 || pos > 6) {
      txNotify("< ERROR: Position must be 0-6, got: " + String(pos));
      return;
    }

    targetPosition = pos;
    txNotify("< TARGET SET: position " + String(pos) + " (current=" + String(currentPosition) + ") - press button or send GO to execute");
    return;
  }

  // --- GO command: execute the move (like pressing the button) ---
  if (U == "GO") {
    txNotify("< GO: current=" + String(currentPosition) + ", target=" + String(targetPosition));

    if (swatchIsReset) {
      swatchIsReset = false;
      if (targetPosition == 0) {
        // Level 10 after reset: needs UV base charge
        txNotify("< CHARGING UP: UV lights ON for " + String(RESET_BASE_UV_TIME) + "ms (reset -> Level 10)");
        int pin265, pin367;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, true);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, true);
        uvLightsActive = true;
        delayWithBlink(RESET_BASE_UV_TIME);
        uvLightsActive = false;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, false);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, false);
        currentPosition = 0;
        txNotify("< MOVE COMPLETE: Now at position 0");
        sendPositionUpdate();
      } else {
        moveTo(currentPosition, targetPosition);
      }
    } else if (currentPosition == 0 && targetPosition == 0) {
      manualBleach();
    } else if (targetPosition != currentPosition) {
      moveTo(currentPosition, targetPosition);
    } else {
      txNotify("< INFO: Already at position " + String(currentPosition));
    }
    return;
  }

  // --- MOVE command: set target AND execute immediately: "MOVE 3" ---
  // Note: MOVE is for positioning only. Use BLEACH command for swatch reset.
  if (U.startsWith("MOVE ")) {
    String posStr = trimStr(line.substring(5));
    int pos = posStr.toInt();

    if (pos < 0 || pos > 6) {
      txNotify("< ERROR: Position must be 0-6, got: " + String(pos));
      return;
    }

    targetPosition = pos;
    txNotify("< MOVE CMD: current=" + String(currentPosition) + ", target=" + String(targetPosition) +
             (swatchIsReset ? ", swatchReset=YES" : ""));

    if (swatchIsReset) {
      // After a swatch reset, always accept the move (even to position 0)
      swatchIsReset = false;
      if (targetPosition == 0) {
        // Level 10 after reset: needs UV base charge
        txNotify("< CHARGING UP: UV lights ON for " + String(RESET_BASE_UV_TIME) + "ms (reset -> Level 10)");
        int pin265, pin367;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, true);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, true);
        uvLightsActive = true;
        delayWithBlink(RESET_BASE_UV_TIME);
        uvLightsActive = false;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, false);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, false);
        currentPosition = 0;
        txNotify("< MOVE COMPLETE: Now at position 0");
        sendPositionUpdate();
      } else {
        // Levels 9-4: existing forwardTimes are already correct from pos 0
        moveTo(currentPosition, targetPosition);
      }
    } else if (targetPosition != currentPosition) {
      moveTo(currentPosition, targetPosition);
    } else {
      txNotify("< INFO: Already at position " + String(currentPosition));
    }
    return;
  }

  // --- BLEACH command: manual bleach anytime (same as button at pos 0) ---
  if (U == "BLEACH") {
    txNotify("< BLUETOOTH COMMAND: Manual bleach");
    manualBleach();
    return;
  }

  // --- STATUS ---
  if (U == "STATUS") {
    txNotify("< STATUS: current=" + String(currentPosition) +
             ", target=" + String(targetPosition) +
             ", btConn=" + String(SerialBT.hasClient() ? "YES" : "NO") +
             ", debug=" + String(debug ? "ON" : "OFF") +
             ", btDebug=" + String(btDebug ? "ON" : "OFF"));
    sendPositionUpdate();
    return;
  }

  // --- Debug toggles ---
  if (U == "DEBUG ON") {
    debug = true;
    txNotify("< OK: Debug ON");
    return;
  }
  if (U == "DEBUG OFF") {
    debug = false;
    txNotify("< OK: Debug OFF");
    return;
  }
  if (U == "BT DEBUG ON" || U == "BTDEBUG ON") {
    btDebug = true;
    txNotify("< OK: Bluetooth debug ON");
    return;
  }
  if (U == "BT DEBUG OFF" || U == "BTDEBUG OFF") {
    btDebug = false;
    txNotify("< OK: Bluetooth debug OFF");
    return;
  }

  // --- STOP / ALL OFF ---
  if (U == "STOP") {
    Command c{};
    c.type = CMD_STOP;
    if (gCmdQueue) xQueueSend(gCmdQueue, &c, 0);
    txNotify("< QUEUED: STOP");
    return;
  }

  if (U == "ALL OFF" || U == "ALLOFF") {
    Command c{};
    c.type = CMD_ALL_OFF;
    if (gCmdQueue) xQueueSend(gCmdQueue, &c, 0);
    txNotify("< QUEUED: ALL OFF");
    return;
  }

  // --- MAP command (from original) ---
  if (U.startsWith("MAP ")) {
    String rest = trimStr(line.substring(4));
    auto parts = splitWS(rest);
    if (parts.size() != 2) {
      txNotify("< ERR: usage MAP <label> <pin>");
      return;
    }
    int p = parts[1].toInt();
    if (p == 0 && parts[1] != "0") {
      txNotify("< ERR: invalid pin");
      return;
    }
    Command c{};
    c.type = CMD_MAP;
    c.mapPin = p;
    strncpy(c.label, parts[0].c_str(), sizeof(c.label) - 1);
    c.label[sizeof(c.label) - 1] = 0;
    if (gCmdQueue) xQueueSend(gCmdQueue, &c, 0);
    txNotify("< QUEUED: MAP");
    return;
  }

  // --- GPIO command (from original) ---
  if (U.startsWith("GPIO ")) {
    String rest = trimStr(line.substring(5));
    auto parts = splitWS(rest);
    if (parts.size() != 2) {
      txNotify("< ERR: usage GPIO <pin> HIGH|LOW");
      return;
    }
    int pin = parts[0].toInt();
    if (pin == 0 && parts[0] != "0") {
      txNotify("< ERR: invalid pin");
      return;
    }
    String levU = upperStr(parts[1]);
    bool high;
    if (levU == "HIGH" || levU == "ON") high = true;
    else if (levU == "LOW" || levU == "OFF") high = false;
    else {
      txNotify("< ERR: level must be HIGH/LOW");
      return;
    }
    Command c{};
    c.type = CMD_GPIO_SET;
    c.pin = pin;
    c.level = high;
    if (gCmdQueue) xQueueSend(gCmdQueue, &c, 0);
    txNotify("< QUEUED: GPIO");
    return;
  }

  // --- LED command (from original) ---
  if (U.startsWith("LED ")) {
    String rest = trimStr(line.substring(4));
    auto parts = splitWS(rest);
    if (parts.size() < 3) {
      txNotify("< ERR: usage LED <label> ON <ms>");
      return;
    }
    String onU = upperStr(parts[1]);
    if (onU != "ON") {
      txNotify("< ERR: expected ON");
      return;
    }
    String msStr = parts[2];
    msStr.replace("ms", "");
    msStr.replace("MS", "");
    int dur = msStr.toInt();
    if (dur <= 0) {
      txNotify("< ERR: invalid duration");
      return;
    }
    Command c{};
    c.type = CMD_LED_ON;
    c.duration = (uint32_t)dur;
    strncpy(c.label, parts[0].c_str(), sizeof(c.label) - 1);
    c.label[sizeof(c.label) - 1] = 0;
    if (gCmdQueue) xQueueSend(gCmdQueue, &c, 0);
    txNotify("< QUEUED: LED");
    return;
  }

  txNotify("< ERR: Unknown command. Valid: MOVE <0-6>, BLEACH (swatch reset), POS <0-6>, GO, STATUS, STOP, DEBUG ON/OFF, BT DEBUG ON/OFF, MAP, GPIO, LED");
}

void setup() {
  Serial.begin(115200);
  delay(200);

  // Initialize LED pins
  for (size_t i = 0; i < ALL_PINS_LEN; ++i) {
    pinMode(ALL_PINS[i], OUTPUT);
    digitalWrite(ALL_PINS[i], LOW);
  }

  // Initialize button
  pinMode(BUTTON_PIN, INPUT);  // Button connects to 3V3, no pull-up needed

  // Initialize onboard LED
  pinMode(ONBOARD_LED, OUTPUT);
  digitalWrite(ONBOARD_LED, LOW);

  // Create FreeRTOS command queue (same as original)
  gCmdQueue = xQueueCreate(32, sizeof(Command));

  // Start Bluetooth with connection callback
  SerialBT.register_callback(btCallback);
  SerialBT.begin(DEVICE_NAME);

  Serial.println("[Bluetooth] ColorReactor ready - pair with: " + DEVICE_NAME);
  Serial.println("[Hardware] Button on pin " + String(BUTTON_PIN));
  Serial.println("[Commands] MOVE <0-6>, BLEACH (swatch reset), POS <0-6>, GO, STATUS, STOP");
  Serial.println("[Commands] DEBUG ON/OFF, BT DEBUG ON/OFF, MAP, GPIO, LED");
  Serial.println("[State] Starting at position 0");
}

void loop() {
  // ---- USB Serial line reader (same as original) ----
  static String serialBuf;
  while (Serial.available()) {
    char ch = (char)Serial.read();
    if (ch == '\n') {
      String line = serialBuf;
      serialBuf = "";
      line.trim();
      if (line.length()) {
        Serial.print("[USB_RX] ");
        Serial.println(line);
        parseCommand(line, "USB");
      }
    } else if (ch != '\r') {
      serialBuf += ch;
      if (serialBuf.length() > 256) serialBuf.remove(0);
    }
  }
  // ---- end USB Serial reader ----

  // ---- Bluetooth line reader ----
  static String btBuf;
  while (SerialBT.available()) {
    char ch = (char)SerialBT.read();
    if (ch == '\n') {
      String line = btBuf;
      btBuf = "";
      line.trim();
      if (line.length()) {
        btLog("Raw bytes received, parsed line: [" + line + "] len=" + String(line.length()));
        parseCommand(line, "BT");
      }
    } else if (ch != '\r') {
      btBuf += ch;
      if (btBuf.length() > 256) btBuf.remove(0);
    }
  }
  // ---- end Bluetooth reader ----

  // ---- Drain queued commands (same as original) ----
  Command c;
  while (gCmdQueue && xQueueReceive(gCmdQueue, &c, 0) == pdTRUE) {
    switch (c.type) {
      case CMD_ALL_OFF:
        activePulses.clear();
        allOff();
        txNotify("< OK: ALL OFF");
        break;

      case CMD_STOP:
        {
          activePulses.clear();
          allOff();
          Command dump;
          while (gCmdQueue && xQueueReceive(gCmdQueue, &dump, 0) == pdTRUE) { /* discard */ }
          txNotify("< OK: STOPPED (all outputs LOW, queue cleared)");
        }
        break;

      case CMD_MAP:
        {
          String label = String(c.label);
          labelToPin[label] = c.mapPin;
          safePinModeOutput(c.mapPin);
          txNotify("< OK: MAP " + label + " -> " + String(c.mapPin));
        }
        break;

      case CMD_GPIO_SET:
        setPinLevel(c.pin, c.level);
        txNotify("< OK: GPIO " + String(c.pin) + " " + (c.level ? "HIGH" : "LOW"));
        break;

      case CMD_LED_ON:
        {
          String label = String(c.label);
          if (label == "wash") {
            const char* washPins[] = { "450nm", "522nm", "657nm", "632nm", "727nm" };
            for (const char* l : washPins) {
              int pin;
              if (resolveLabelPin(l, pin)) {
                schedulePulse(pin, c.duration);
              }
            }
            txNotify("< OK: LED WASH ON " + String(c.duration) + "ms (450nm + 522nm + 657nm)");
            break;
          }

          int pin;
          if (!resolveLabelPin(label, pin)) {
            txNotify("< ERR: unknown label " + label);
            break;
          }
          schedulePulse(pin, c.duration);
          txNotify("< OK: LED " + label + " ON " + String(c.duration) + "ms (pin " + String(pin) + ")");
        }
        break;

      default: break;
    }
  }

  // Service active pulses (same as original)
  servicePulses();

  // Update blinking LED for UV indicator (same as original)
  updateBlinkingLED();

  // ---- Button handling (same logic as original's potentiometer + button) ----
  // targetPosition is set by Bluetooth POS command instead of potentiometer

  // Debug logging
  if (debug) logDebugInfo();

  if (buttonPressed()) {
    txNotify("< BUTTON PRESSED: current=" + String(currentPosition) + ", target=" + String(targetPosition));

    if (swatchIsReset) {
      // After a swatch reset, any button press moves to target
      swatchIsReset = false;
      if (targetPosition == 0) {
        // Level 10 after reset: needs UV base charge
        txNotify("< CHARGING UP: UV lights ON for " + String(RESET_BASE_UV_TIME) + "ms (reset -> Level 10)");
        int pin265, pin367;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, true);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, true);
        uvLightsActive = true;
        delayWithBlink(RESET_BASE_UV_TIME);
        uvLightsActive = false;
        if (resolveLabelPin("265nm", pin265)) setPinLevel(pin265, false);
        if (resolveLabelPin("367nm", pin367)) setPinLevel(pin367, false);
        currentPosition = 0;
        txNotify("< MOVE COMPLETE: Now at position 0");
        sendPositionUpdate();
      } else {
        moveTo(currentPosition, targetPosition);
      }
    } else if (currentPosition == 0 && targetPosition == 0) {
      // Special case: Manual bleach when at position 0 with target 0
      manualBleach();
    } else if (targetPosition != currentPosition) {
      moveTo(currentPosition, targetPosition);
    } else {
      txNotify("< INFO: Already at position " + String(currentPosition));
    }
  }
  // ---- end Button handling ----

  delay(1);
}
