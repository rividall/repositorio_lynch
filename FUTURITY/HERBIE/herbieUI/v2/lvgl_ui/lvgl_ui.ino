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
// --
void setup() {
  FastLED.addLeds<WS2812B, DATA_PIN, RGB>(leds, NUM_LEDS);
  dht.begin();
  Serial.begin(115200);

  LCD_Init();
  Lvgl_Init();
  ui_init();
}

void loop() {
  tempHum();
  soilM();
  ledSt();
  Timer_Loop();
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
  soilMoistureValue = map(sm, 0, 4095, 0, 255);
  lv_arc_set_value(ui_Arc1,soilMoistureValue);
  lv_label_set_text(ui_Label3,String(soilMoistureValue).c_str());
}

void tempHum() {
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  lv_label_set_text(ui_temp,String(t).c_str());
  lv_label_set_text(ui_hum,String(h).c_str());
}
