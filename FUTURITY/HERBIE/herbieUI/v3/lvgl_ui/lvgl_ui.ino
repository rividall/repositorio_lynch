#include "Display_ST7789.h"
#include "LVGL_Driver.h"
#include "ui.h"
#include <FastLED.h>  // Librería FastLed. Documentación; https://github.com/FastLED/FastLED/wiki/Basic-usage

// LED CONTROL
#define NUM_LEDS 1  // Cantidad de leds onboard
#define DATA_PIN 8  // Pines datos cada tira
CRGB leds[1];
int startmill = 300;
bool thresh = false;
int timer = 50;
int bgt = 10;
int fader = 5;
// SOIL MOISTURE
#define ANALOG_PIN 1  // Use GPIO1 as the analog input
int soilMoistureValue = 0;
// DHT
#include <DHT.h>
#define DHTPIN 0
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
float h = 0;
float t = 0;
// GAS lvl
int gasValue = 0;
// LIGHT
int lightLvl = 0;
// --
void setup() {
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
  dht.begin();
  Serial.begin(115200);

  LCD_Init();
  Lvgl_Init();
  ui_init();

  wirelessSetup();
}

void loop() {
  gasM();
  tempHum();
  soilM();
  ledSt();
  lightLVL();
  Timer_Loop();

  wirelessLoop();
  delay(5);
}

void ledSt() {
  unsigned long cmillis = millis();
  if (cmillis - startmill >= timer) {
    startmill = cmillis;
    if (thresh == true) {
      bgt += fader;
    } else {
      bgt -= fader;
    }
  }
  if (bgt >= 245) {
    thresh = false;
  }
  if (bgt <= 5) {
    thresh = true;
  }
  fill_solid(leds, NUM_LEDS, CRGB(80, 230, soilMoistureValue));
  FastLED[0].showLeds(bgt);
}

void soilM() {
  int sm = analogRead(1);
  soilMoistureValue = map(sm, 0, 4095, 270, 0);
  lv_arc_set_value(ui_moistG, soilMoistureValue);
  lv_label_set_text(ui_moistN, String(soilMoistureValue).c_str());
}

void tempHum() {
  h = dht.readHumidity();
  t = dht.readTemperature();
  lv_label_set_text(ui_tempN, String(t).c_str());
  lv_label_set_text(ui_humN, String(h).c_str());
}

void gasM() {
  int g = analogRead(2);
  gasValue = map(g, 0, 4095, 0, 255);
  lv_label_set_text(ui_gasN, String(gasValue).c_str());
}

void lightLVL(){
  lightLvl = map(analogRead(3),0,1024,100,0);
}
