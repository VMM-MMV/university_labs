#pragma once

#include <Arduino.h>

class PWMController {
  private:
    int _pin;

  public:
    PWMController(int pin);

    void write_percent(float percentage);

};