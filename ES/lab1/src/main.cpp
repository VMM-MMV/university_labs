#include <Arduino.h>
#include "Tachometer.h"

const int tachoPin = 3;

void setup() {
  Serial.begin(9600);
  
  Tachometer::begin(tachoPin);
}

void loop() {
  delay(1000);
  
  unsigned long rpm = Tachometer::getRPM();
  
  Serial.print("RPM: ");
  Serial.println(rpm);
}