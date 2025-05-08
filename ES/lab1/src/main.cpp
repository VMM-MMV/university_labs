#include <Arduino.h>
#include "Tachometer.h"
#include "PWMController.h"

const int tachoPin = 2;
PWMController pwmController(9);

void setup() {
  Serial.begin(9600);
  Tachometer::begin(tachoPin);
}

void loop() {
  delay(1000);
  pwmController.write_percent(10);
  
  unsigned long rpm = Tachometer::getRPM();
  
  Serial.print("RPM: ");
  Serial.println(rpm);
}