// Refactored from original code by Ricardo Vidal Lynch
#include "esp32-hal-gpio.h"
#include <FastLED.h>

#define NUM_LEDS 5
#define DATA_PIN 22
#define B1_PIN 33
#define B2_PIN 4
#define B3_PIN 25
#define B4_PIN 32
#define B5_PIN 14
#define B6_PIN 12
extern int currentPotValue;
CRGB leds[NUM_LEDS];
int activeFlashingIndex = -1;

#define GAME_BUTTON_COUNT 4
const int buttonPins[GAME_BUTTON_COUNT] = { B1_PIN, B2_PIN, B3_PIN, B4_PIN };
const int ledIndices[GAME_BUTTON_COUNT] = { 0, 1, 2, 3 };
const int CONFIRM_BUTTON = B5_PIN;
const int DELETE_BUTTON = B6_PIN;

enum GameState { IDLE,
                 SHOW_SEQUENCE,
                 WAIT_INPUT,
                 WIN,
                 LOSE,
                 MIDI_PAD };
enum GameMode { GAME_NONE,
                GAME_MEMORY,
                GAME_MIDI,
                GAME_POT,
                GAME_MULTI };

GameState gameState = IDLE;
GameMode currentGame = GAME_NONE;

bool gameStart = false;
int sequence[GAME_BUTTON_COUNT];
int userInput[GAME_BUTTON_COUNT];
int userInputLen = 0;
int showStep = 0;
unsigned long lastStepTime = 0;
unsigned long showStartTime = 0;
unsigned long stepInterval = 600;
unsigned long showDuration = 1000;

int breathLevel = 50;
bool breathingUp = true;
unsigned long lastBreathUpdate = 0;
const int breathSpeed = 10;

unsigned long ledOnTimes[GAME_BUTTON_COUNT] = { 0 };
const unsigned long midiGlowDuration = 100;

unsigned long lastButtonTimes[GAME_BUTTON_COUNT + 2] = { 0 };
const unsigned long debounceDelay = 350;

void clearLeds() {
  for (int i = 0; i < NUM_LEDS; i++) leds[i] = CHSV(0, 0, 0);
}

void generateSequence() {
  int pool[GAME_BUTTON_COUNT] = { 0, 1, 2, 3 };
  for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
    int idx = random(0, GAME_BUTTON_COUNT - i);
    sequence[i] = pool[idx];
    for (int j = idx; j < GAME_BUTTON_COUNT - i - 1; j++) {
      pool[j] = pool[j + 1];
    }
  }
}

bool readButton(int pin, int idx) {
  if (digitalRead(pin) == LOW && millis() - lastButtonTimes[idx] > debounceDelay) {
    lastButtonTimes[idx] = millis();
    return true;
  }
  return false;
}

void writeSerial(const char* message) {
  Serial.println(message);
}

void serialIn() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    Serial.println(command);

    if (command == "MEM") {
      currentGame = GAME_MEMORY;
      gameStart = true;
    } else if (command == "MIDI") {
      currentGame = GAME_MIDI;
      gameState = MIDI_PAD;
    } else if (command == "MULT") {
      currentGame = GAME_MULTI;
      gameState = IDLE;
      activeFlashingIndex = -1;
    } else if (command == "POTE") {
      currentGame = GAME_POT;
    } else if (command == "i") {
      currentGame = GAME_NONE;
      gameState = IDLE;
    }

    clearLeds();
    FastLED.show();
  }
}

void handleIdleAnimation() {
  if (millis() - lastBreathUpdate >= breathSpeed) {
    breathLevel++;
    if (breathLevel >= 255) breathLevel = 0;
    for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
      uint8_t hue = (breathLevel + i * 64) % 255;
      leds[ledIndices[i]] = CHSV(hue, 255, 255);
    }
    lastBreathUpdate = millis();
  }
}

void handleMemoryGame() {
  switch (gameState) {
    case IDLE:
      if (gameStart) {
        generateSequence();
        showStep = 0;
        lastStepTime = millis();
        userInputLen = 0;
        gameState = SHOW_SEQUENCE;
        clearLeds();
        FastLED.show();
      }
      break;

    case SHOW_SEQUENCE:
      if (showStep < GAME_BUTTON_COUNT) {
        if (millis() - lastStepTime >= stepInterval) {
          leds[ledIndices[sequence[showStep]]] = CHSV(sequence[showStep] * 60, 255, 255);
          FastLED.show();
          lastStepTime = millis();
          showStep++;
        }
      } else {
        if (millis() - lastStepTime >= showDuration) {
          clearLeds();
          FastLED.show();
          gameState = WAIT_INPUT;
        }
      }
      break;

    case WAIT_INPUT:
      clearLeds();
      for (int i = 0; i < userInputLen; i++) {
        leds[ledIndices[userInput[i]]] = CHSV(userInput[i] * 60, 255, 255);
      }
      if (readButton(DELETE_BUTTON, GAME_BUTTON_COUNT)) {
        userInputLen = 0;
      }
      for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
        if (readButton(buttonPins[i], i)) {
          bool found = false;
          int foundIndex = -1;
          for (int j = 0; j < userInputLen; j++) {
            if (userInput[j] == i) {
              found = true;
              foundIndex = j;
              break;
            }
          }
          if (found) {
            for (int j = foundIndex; j < userInputLen - 1; j++) {
              userInput[j] = userInput[j + 1];
            }
            userInputLen--;
          } else if (userInputLen < GAME_BUTTON_COUNT) {
            userInput[userInputLen++] = i;
          }
        }
      }
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1) && userInputLen == GAME_BUTTON_COUNT) {
        bool correct = true;
        for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
          if (userInput[i] != sequence[i]) {
            correct = false;
            break;
          }
        }

        writeSerial(correct ? "win" : "lose");

        // Flash all LEDs green or red
        for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
          leds[ledIndices[i]] = CHSV(correct ? 96 : 0, 255, 255);  // 96 = green, 0 = red
        }
        FastLED.show();
        delay(600);

        clearLeds();
        FastLED.show();

        gameStart = false;
        currentGame = GAME_NONE;
        gameState = IDLE;
        lastStepTime = millis();
      }
      break;

    case WIN:
    case LOSE:
      break;
  }
}

void user_setup(void) {
  pinMode(B1_PIN, INPUT_PULLUP);
  pinMode(B2_PIN, INPUT_PULLUP);
  pinMode(B3_PIN, INPUT_PULLUP);
  pinMode(B4_PIN, INPUT_PULLUP);
  pinMode(B5_PIN, INPUT_PULLUP);
  pinMode(B6_PIN, INPUT_PULLUP);
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);
  randomSeed(analogRead(0));
}



void handleMultiGame() {
  // Turn on all buttons initially
  for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
    leds[ledIndices[i]] = CHSV(i * 60, 255, 80);
  }

  // Flash the selected button
  if (activeFlashingIndex >= 0) {
    int brightness = (millis() / 300) % 2 ? 255 : 255;
    leds[ledIndices[activeFlashingIndex]] = CHSV(activeFlashingIndex * 60, 255, brightness);
  }

  // Check for button presses to select new flashing button
  for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
    if (readButton(buttonPins[i], i)) {
      activeFlashingIndex = i;
    }
  }

  // Confirm selection
  if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1) && activeFlashingIndex >= 0) {
    switch (activeFlashingIndex) {
      case 0: writeSerial("btn2"); break;
      case 1: writeSerial("btn4"); break;
      case 2: writeSerial("btn3"); break;
      case 3: writeSerial("btn1"); break;
    }
    currentGame = GAME_NONE;
    gameState = IDLE;
    clearLeds();
    activeFlashingIndex = -1;
  }
}


void handleMidiGame() {
  clearLeds();
  for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
    if (readButton(buttonPins[i], i)) {
      ledOnTimes[i] = millis();
      switch (i) {
        case 0: writeSerial("btn2"); break;
        case 1: writeSerial("btn4"); break;
        case 2: writeSerial("btn3"); break;
        case 3: writeSerial("btn1"); break;
      }
    }
    if (millis() - ledOnTimes[i] < 200) {
      leds[ledIndices[i]] = CHSV(i * 60, 255, 255);
    }
  }

  if (readButton(DELETE_BUTTON, GAME_BUTTON_COUNT)) {
    writeSerial("EOG");
    currentGame = GAME_NONE;
    gameState = IDLE;
    clearLeds();
  }
}

void handlePotGame() {
  if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
    int potVal = (currentPotValue < 2048) ? 0 : 1;
    Serial.println(potVal);
    currentGame = GAME_NONE;
    gameState = IDLE;
    clearLeds();
  }
}

void user_loop(void) {
  serialIn();
  switch (currentGame) {
    case GAME_MEMORY: handleMemoryGame(); break;
    case GAME_MIDI: handleMidiGame(); break;
    case GAME_POT: handlePotGame(); break;
    case GAME_MULTI: handleMultiGame(); break;
    case GAME_NONE:
    default:
      handleIdleAnimation();
      break;
  }
  FastLED.show();
}
