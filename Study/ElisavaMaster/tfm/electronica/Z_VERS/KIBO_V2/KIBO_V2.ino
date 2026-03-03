#include <WiFi.h>
#include "esp_bt.h"
#include <SPI.h>
#include <TFT_eSPI.h>
TFT_eSPI tft = TFT_eSPI();

#define device_A_CS 5
#define device_B_CS 2
#define BL1 19
#define BL2 19
#define POT_PIN 34

extern void user_setup(void);  // Functions in the user*.cpp files
extern void user_loop(void);

#define SCREEN_X_START 0
#define SCREEN_X_END SCREEN_WIDTH  // Badly named, actually the "eye" width!
#define SCREEN_Y_START 0
#define SCREEN_Y_END SCREEN_HEIGHT  // Actually "eye" height

// A simple state machine is used to control eye blinks/winks:
#define NOBLINK 0  // Not currently engaged in a blink
#define ENBLINK 1  // Eyelid is currently closing
#define DEBLINK 2  // Eyelid is currently opening

#define BUFFER_SIZE 1024  // 128 to 1024 seems optimum

#ifdef USE_DMA
#define BUFFERS 2  // 2 toggle buffers with DMA
#else
#define BUFFERS 1  // 1 buffer for no DMA
#endif

uint16_t pbuffer[BUFFERS][BUFFER_SIZE];  // Pixel rendering buffer
                                         // DMA buffer selection

// This struct is populated in config.h
typedef struct {      // Struct is defined before including config.h --
  int8_t select;      // pin numbers for each eye's screen select line
  int8_t wink;        // and wink button (or -1 if none) specified there,
  uint8_t rotation;   // also display rotation and the x offset
  int16_t xposition;  // position of eye on the screen
} eyeInfo_t;
#include "config.h"
typedef struct {
  uint8_t state;       // NOBLINK/ENBLINK/DEBLINK
  uint32_t duration;   // Duration of blink state (micros)
  uint32_t startTime;  // Time (micros) of last state change
} eyeBlink;
struct {              // One-per-eye structure
  int16_t tft_cs;     // Chip select pin for each display
  eyeBlink blink;     // Current blink/wink state
  int16_t xposition;  // x position of eye image
} eye[NUM_EYES];

bool dmaBuf = 0;
uint32_t startTime;

void pwm_init() {
  ledcSetup(1, 1000, 8);
  ledcSetup(2, 1000, 8);
  ledcAttachPin(BL1, 1);
  ledcAttachPin(BL2, 2);
}

void LED_PWM(unsigned char i) {
  ledcWrite(1, i);
  ledcWrite(2, i);
  delay(10);
}

void setup() {
  Serial.begin(9600);
  for (int j = 0; j < 10; j++) {
    Serial.println("");
    delay(20);
  }
  disableComms();
  pinMode(BL1, OUTPUT);
  pinMode(BL2, OUTPUT);
  pinMode(device_A_CS, OUTPUT);
  pinMode(device_B_CS, OUTPUT);
  digitalWrite(BL1, HIGH);
  digitalWrite(BL2, HIGH);

  digitalWrite(device_A_CS, LOW);  // we need to 'init' all displays
  digitalWrite(device_B_CS, LOW);
  pwm_init();
  tft.init();

  digitalWrite(device_A_CS, HIGH);
  digitalWrite(device_B_CS, HIGH);

  initEyes();
  if (NUM_EYES > 1) digitalWrite(eye[1].tft_cs, HIGH);

  for (uint8_t e = 0; e < NUM_EYES; e++) {
    digitalWrite(eye[e].tft_cs, LOW);
    tft.setRotation(eyeInfo[e].rotation);
    tft.fillScreen(TFT_BLACK);
    digitalWrite(eye[e].tft_cs, HIGH);
  }
  user_setup();
  LED_PWM(255);
}

void loop() {
  updateEye();
}

void disableComms() {
  esp_bt_controller_disable();
  esp_bt_controller_deinit();
  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);
}
