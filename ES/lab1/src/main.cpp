#include <Arduino.h>
#include "Led.h"
#include "IO.h"
#include <stdio.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Keypad.h>
#include "KeypadWrapper.h"
#include "LCD.h"
#include "KLRedirector.h"

Led greenLed(13);
Led redLed(12);

KeypadWrapper keypad;
LCD lcd;
KLRedirector klRedirector(lcd, keypad);

const char* rightCode = "1234";

void setup() {
  Serial.begin(9600);
  
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  klRedirector.init();
}

void loop() {
  char input[5] = {0};
  
  lcd.clear();
  printf("Enter code: ");
  
  scanf("%4s", input);
  
  lcd.clear();
  
  if (strcmp(input, rightCode) == 0) {
    printf("Code Valid!");
    greenLed.on();
    redLed.off();
  } else {
    printf("Code Invalid!");
    redLed.on();
    greenLed.off();
  }

  delay(2000);
}
