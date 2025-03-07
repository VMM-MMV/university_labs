#include "KeyboardButton.h"
#include <Arduino.h>
#include "KeypadWrapper.h"

KeyboardButton::KeyboardButton(int pin) : pin(pin) {}

KeypadWrapper keypad;

void KeyboardButton::setPin(int newPin) {
    pin = newPin;
}

bool KeyboardButton::isClicked() {
    char key = keypad.getKey();
    if (key == 0) return 0;
    int key_int = key - '0';
    Serial.print(key_int);
    Serial.println(" ");
    Serial.println(pin);
    return key_int == pin;
}

void KeyboardButton::setup() {
}