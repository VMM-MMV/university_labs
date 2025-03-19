#include "Button.h"
#include <Arduino.h>

Button::Button(int pin) : pin(pin), lastState(HIGH), lastDebounceTime(0) {}

void Button::setup() {
    pinMode(pin, INPUT_PULLUP);
}

bool Button::isClicked() {
    return !digitalRead(pin);
}

bool Button::isClickedDB() {
    const int debounceDelay = 50; // ms
    bool currentState = !digitalRead(pin);

    if (currentState != lastState) {
        lastDebounceTime = millis();
    }

    if ((millis() - lastDebounceTime) > debounceDelay) {
        if (currentState && !buttonPressed) {
            buttonPressed = true;
            lastState = currentState;
            return true;
        }
    }

    if (!currentState) {
        buttonPressed = false;
    }

    lastState = currentState;
    return false;
}
