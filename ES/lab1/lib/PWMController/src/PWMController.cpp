#include "PWMController.h"

PWMController::PWMController(int pin) {
  _pin = pin;
  pinMode(_pin, OUTPUT);
}

void PWMController::write_percent(float percentage) {
  if (percentage < 0) percentage = 0;
  if (percentage > 100) percentage = 100;
  int pwm = (percentage * 255) / 100;
  analogWrite(_pin, pwm);
}