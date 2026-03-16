#include <Adafruit_NeoPixel.h>

Adafruit_NeoPixel strip = Adafruit_NeoPixel(3, 7, NEO_GRB + NEO_KHZ800);
int sensorValue = 0;  // value read from the pot

const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

void setup() {
  Serial.begin(9600);
  pinMode(A0, INPUT_PULLUP);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(A0);
  // print the results to the serial monitor:
  Serial.print("sensor = ");
  Serial.println(sensorValue);

  if (sensorValue < 28) {
    Serial.println("leds triggered");
    colorWipe(strip.Color(255, 0, 0), 25);
    colorWipe(strip.Color(0, 0, 0), 25);
  }
}

void colorWipe(uint32_t c, uint8_t wait) {
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
    delay(wait);
  }
}