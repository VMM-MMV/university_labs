#pragma once

#include <Arduino.h>
#include "LCD.h"
#include "KeypadWrapper.h"

class KLRedirector {
public:
    KLRedirector(LCD &lcd, KeypadWrapper &keypad);
    void init();

private:
    LCD &lcd;
    KeypadWrapper &keypad;

    int serial_putchar(char c, FILE* f);
    int serial_getchar(FILE* f);

    FILE serial_stream;
};
