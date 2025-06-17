// microcontroller: ESP32-WROOM-32
// displays: 2 0.71 inch 3.3V TFT 160*160 pixels GC9D01 controller
//
// sequential display of the sketch by directing frames to CS pins
// center x-y-coordinates of all devices: x = 120 and y = 120

// pin layout:
// both displays     ESP32
//     GND ---------- GND
//     VCC ---------- 3.3V
//     SCL ---------- 18
//     SDA ---------- 23
//     RES ---------- 21
//.    RES2 --------- 27
//     DC  ---------- 26
//     BLK ---------- VIN
//     CSA ---------- 5
//.    CSB ---------- 2

#include <SPI.h>
#include <TFT_eSPI.h>
#include "EYEA.h"
#include "EYEB.h"
TFT_eSPI tft = TFT_eSPI();

#define device_A_CS 5
#define device_B_CS 2

#define BL1 19
#define BL2 19

// some extra colors
#define BLACK 0x0000
#define BLUE 0x001F
#define RED 0xF800
#define GREEN 0x07E0
#define CYAN 0x07FF
#define MAGENTA 0xF81F
#define YELLOW 0xFFE0
#define WHITE 0xFFFF
#define ORANGE 0xFBE0
#define GREY 0x84B5
#define BORDEAUX 0xA000
#define DINOGREEN 0x2C86
#define WHITE 0xFFFF

int frameTime = 70;
int j;

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
uint32_t startTime;

void pwm_init() {
  //设置通道号，频率为1000HZ，分辨率为8位
  ledcSetup(1, 1000, 8);
  ledcSetup(2, 1000, 8);
  //将通道产生的PWM波映射到BL引脚上
  ledcAttachPin(BL1, 1);
  ledcAttachPin(BL2, 2);
}

void LED_PWM(unsigned char i) {
  ledcWrite(1, i);
  ledcWrite(2, i);
  delay(10);
}

void led_breathing() {
  for (int i = 0; i <= 255; i++) {
    ledcWrite(1, i);
    ledcWrite(2, i);
    delay(10);
  }
  for (int i = 255; i >= 0; i--) {
    ledcWrite(1, i);
    ledcWrite(2, i);
    delay(10);
  }
}

void PWM_test() {
  digitalWrite(device_A_CS, LOW);
  tft.fillScreen(BLUE);  // we need to 'init' all displays
  digitalWrite(device_A_CS, HIGH);
  //  tft.setRotation (3);

  digitalWrite(device_B_CS, LOW);
  tft.fillScreen(RED);
  digitalWrite(device_B_CS, HIGH);
}

void setup() {

  Serial.begin(9600);
  for (j = 0; j < 10; j++) {
    Serial.println("0");
    delay(20);
  }
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
  //  tft.setRotation (3);
  tft.fillScreen(BLACK);
  //  tft.pushImage (0, 0,160, 160, bmp1);
  tft.setTextColor(YELLOW, BLACK);

  digitalWrite(device_A_CS, HIGH);
  digitalWrite(device_B_CS, HIGH);

  LED_PWM(255);
}

char i = 1;
void loop() {
  LED_PWM(255);
  digitalWrite(device_B_CS, LOW);
  tft.setRotation(0);
  tft.fillScreen(BLUE);
  digitalWrite(device_B_CS, HIGH);

  digitalWrite(device_A_CS, LOW);
  tft.setRotation(0);
  tft.fillScreen(RED);
  digitalWrite(device_A_CS, HIGH);

  delay(2000);
}
