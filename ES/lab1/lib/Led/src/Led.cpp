#include "Led.h"
#include <Arduino.h>

Led::Led(int pin) : pin(pin) {
    pinMode(pin, OUTPUT);
    state = LOW;
}

void Led::on() {
    state = HIGH;
    digitalWrite(pin, state);
}

void Led::off() {
    state = LOW;
    digitalWrite(pin, state);
}

void Led::blink(int delayTime) {
    on();
    delay(delayTime);
    off();
}

void Led::toggle() {
    state = !state;
    digitalWrite(pin, state);
}

bool Led::getState() {
    return state;
}
