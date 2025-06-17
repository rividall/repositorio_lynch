// Made by Ricardo Vidal Lynch
#include "esp32-hal-gpio.h"
#include <FastLED.h>

#define NUM_LEDS 5  // Led 3 always off
#define DATA_PIN 22
#define B1_PIN 33   // Button 1 Naranjo
#define B2_PIN 4  // Button 2 Amarillo
#define B3_PIN 25  // Button 3 Azul
#define B4_PIN 32  // Button 4 verde
#define B5_PIN 14  // Start/Confirm Button
#define B6_PIN 12  // Delete Button

CRGB leds[NUM_LEDS];

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
GameState gameState = IDLE;

enum StepPhase { STEP_ON,
                 STEP_OFF };
StepPhase stepPhase = STEP_ON;

bool gameStart = false;
int sequence[GAME_BUTTON_COUNT];
int userInput[GAME_BUTTON_COUNT];
int userInputLen = 0;
int showStep = 0;
unsigned long lastStepTime = 0;
unsigned long showStartTime = 0;
unsigned long stepInterval = 600;
unsigned long showDuration = 1000;
// IDLE mode breath
int breathLevel = 50;
bool breathingUp = true;
unsigned long lastBreathUpdate = 0;
const int breathSpeed = 10;
const int breathMax = 255;
const int breathMin = 0;
//MIDI
unsigned long ledOnTimes[GAME_BUTTON_COUNT] = { 0 };
const unsigned long midiGlowDuration = 100;
// Debounce
unsigned long lastButtonTimes[GAME_BUTTON_COUNT + 2] = { 0 };
const unsigned long debounceDelay = 350;

// Helpers
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

void serialIn() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    Serial.println(command);
    switch (command) {
      case 'i':
        gameState = IDLE;
        break;
      case 's':
        gameStart = true;
        break;
      case 'x':
        gameState = MIDI_PAD;
        break;
        // Add more cases if needed
    }
    clearLeds();
    FastLED.show();
  }
}
void writeSerial(const char* message) {
  Serial.println(message);
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

void user_loop(void) {
  serialIn();
  switch (gameState) {
    case IDLE:
      // Update breath level every 50ms
      if (millis() - lastBreathUpdate >= breathSpeed) {
        /*if (breathingUp) { // breathe up and down for bgt breath
          breathLevel++;
          if (breathLevel >= breathMax) {
            breathLevel = breathMax;
            breathingUp = false;
          }
        } else {
          breathLevel--;
          if (breathLevel <= breathMin) {
            breathLevel = breathMin;
            breathingUp = true;
          }
        }*/
        breathLevel++;  // only goes up, for rainbow color wheel
        if (breathLevel >= 255) breathLevel = 0;
        // Update LEDs with new brightness
        for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
          uint8_t hue = (breathLevel + i * 64) % 255;
          leds[ledIndices[i]] = CHSV(hue, 255, 255);  // H=0, S=0 = white
        }
        lastBreathUpdate = millis();
      }
      /*
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
        gameStart = true;
        clearLeds();
        FastLED.show();
      }
      // Delete button enters MIDI_PAD mode
      if (readButton(DELETE_BUTTON, GAME_BUTTON_COUNT)) {
        gameState = MIDI_PAD;
        clearLeds();
        FastLED.show();
      }
      */
      if (gameStart) {
        generateSequence();
        showStep = 0;
        stepPhase = STEP_ON;
        lastStepTime = millis();
        showStartTime = 0;
        userInputLen = 0;
        gameState = SHOW_SEQUENCE;
        clearLeds();
        FastLED.show();
      }
      break;
    case SHOW_SEQUENCE:
      if (showStep < GAME_BUTTON_COUNT) {
        if (millis() - lastStepTime >= stepInterval) {
          // Show next LED
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

      // Light up current user selections
      for (int i = 0; i < userInputLen; i++) {
        leds[ledIndices[userInput[i]]] = CHSV(userInput[i] * 60, 255, 255);
      }

      // DELETE_BUTTON clears all inputs
      if (readButton(DELETE_BUTTON, GAME_BUTTON_COUNT)) {
        userInputLen = 0;
      }

      // Toggle input: add if not present, remove if present
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
            // Remove the input
            for (int j = foundIndex; j < userInputLen - 1; j++) {
              userInput[j] = userInput[j + 1];
            }
            userInputLen--;
          } else if (userInputLen < GAME_BUTTON_COUNT) {
            // Add the input
            userInput[userInputLen++] = i;
          }
        }
      }

      // Confirm sequence
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1) && userInputLen == GAME_BUTTON_COUNT) {
        bool correct = true;
        for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
          if (userInput[i] != sequence[i]) {
            correct = false;
            break;
          }
        }
        gameState = correct ? WIN : LOSE;
        lastStepTime = millis();
      }

      break;
    case WIN:
      for (int i = 0; i < GAME_BUTTON_COUNT; i++)
        leds[ledIndices[i]] = CHSV(96, 255, 255);
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
        gameStart = true;
        gameState = IDLE;
      } else if (millis() - lastStepTime > 1500) {
        gameState = IDLE;
        gameStart = false;
        clearLeds();
      }
      break;

    case LOSE:
      for (int i = 0; i < GAME_BUTTON_COUNT; i++)
        leds[ledIndices[i]] = CHSV(0, 255, 255);
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
        gameStart = true;
        gameState = IDLE;
      } else if (millis() - lastStepTime > 1500) {
        gameState = IDLE;
        gameStart = false;
        clearLeds();
      }
      break;

    case MIDI_PAD:
      clearLeds();

      for (int i = 0; i < GAME_BUTTON_COUNT; i++) {
        if (readButton(buttonPins[i], i)) {
          ledOnTimes[i] = millis();  // Store the activation time
        }
        if (millis() - ledOnTimes[i] < midiGlowDuration) {
          leds[ledIndices[i]] = CHSV(i * 60, 255, 255);  // Original color
        }
      }

      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
        clearLeds();
        gameState = IDLE;
      }
      break;
  }
  FastLED.show();
}