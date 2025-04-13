#pragma once
#include <Arduino.h>

class Relay {
  private:
    int pin;
    bool state;

  public:
    Relay(int relayPin);
    void init();
    void on();
    void off();
    bool isOn();
};