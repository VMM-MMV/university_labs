#include <Arduino.h>
#include "KLRedirector.h"

KLRedirector::KLRedirector(LCD &lcd, KeypadWrapper &keypad) 
    : lcd(lcd), keypad(keypad) {}

int KLRedirector::serial_putchar(char c, FILE* f) {
    lcd.print(c);
    return 0;
}

int KLRedirector::serial_getchar(FILE* f) {
    char customKey = keypad.getKey();
  
    while (!customKey) {
      customKey = keypad.getKey();
    }
    
    return customKey;
}

void KLRedirector::init() {
    lcd.init();

    FILE* serial_stream = fdevopen(
        [](char c, FILE* f) -> int { return reinterpret_cast<KLRedirector*>(f->udata)->serial_putchar(c, f); },
        [](FILE* f) -> int { return reinterpret_cast<KLRedirector*>(f->udata)->serial_getchar(f); }
    );

    serial_stream->udata = this;
    stdin = stdout = serial_stream;
}