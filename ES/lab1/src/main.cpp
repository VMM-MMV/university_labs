#include <Arduino.h>
#include "Led.h"
#include "IO.h"
#include <stdio.h>
#include <Arduino.h>

Led led = Led(13);

void setup() {
    Serial.begin(9600);
    delay(500);
    pinMode(13,OUTPUT);
    IO::init();
}

void loop() {
    printf("Enter your command: ");
    char* input = IO::input();

    if (strcmp(input, "led on") == 0) {
        led.on();
    } else if (strcmp(input, "led off") == 0) {
        led.off();
    }
    printf("\n");
}