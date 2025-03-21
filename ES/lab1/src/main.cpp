#include <Arduino.h>
#include "Joystick.h"

const int VRX_PIN = A0;
const int VRY_PIN = A1;

Joystick joystick(VRX_PIN, VRY_PIN);

void setup() {
  Serial.begin(9600);
}

void loop() {
  joystick.acquireData();
  delay(100);
}