#include "esp32-hal-gpio.h"
#include <FastLED.h>

#define NUM_LEDS 5  // Led 3 is always off
#define DATA_PIN 22
#define B1_PIN 4   // Button 1
#define B2_PIN 32  // Button 2
#define B3_PIN 33  // Button 3
#define B4_PIN 25  // Button 4
#define B5_PIN 14  // Start/Confirm Button
#define B6_PIN 12  // Delete Button

CRGB leds[NUM_LEDS];

#define GAME_BUTTON_COUNT 4
const int buttonPins[GAME_BUTTON_COUNT] = { B1_PIN, B2_PIN, B3_PIN, B4_PIN };
const int ledIndices[GAME_BUTTON_COUNT] = { 0, 1, 3, 4 };
const int CONFIRM_BUTTON = B5_PIN;
const int DELETE_BUTTON = B6_PIN;

enum GameState { IDLE,
                 SHOW_SEQUENCE,
                 WAIT_INPUT,
                 WIN,
                 LOSE };
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
  switch (gameState) {
    case IDLE:
      if (readButton(CONFIRM_BUTTON, GAME_BUTTON_COUNT + 1)) {
        gameStart = true;
      }
      if (gameStart) {
        generateSequence();
        showStep = 0;
        stepPhase = STEP_ON;
        lastStepTime = millis();
        showStartTime = 0;
        userInputLen = 0;
        gameState = SHOW_SEQUENCE;
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
  }
  FastLED.show();
}
