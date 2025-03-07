#include "Button.h"
#include <Arduino.h>

Button::Button(int pin) : pin(pin) {}

bool Button::isClicked() {
    return !digitalRead(pin);
}

void Button::setup() {
    pinMode(pin, INPUT_PULLUP);
}