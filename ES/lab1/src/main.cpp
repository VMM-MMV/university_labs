#include <Arduino.h>
#include "Led.h"
#include "IO.h"
#include <stdio.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>
#include <Keypad.h>

const byte ROWS = 4; 
const byte COLS = 4; 

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {4, 5, 6, 7};
byte colPins[COLS] = {8, 9, 10, 11};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

Led ledVerde = Led(13);
Led ledRosu = Led(12);
LiquidCrystal_I2C lcd(0x27, 16, 2);

const String codCorect = "1234";  
String codIntroduc = "";  

void setup() {
  Serial.begin(9600);
  delay(500);

  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);

  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("Introduceti cod:");
}

void loop() {
  char customKey = customKeypad.getKey();
  
  if (customKey) {
    lcd.setCursor(0, 1);
    
    if (customKey == '#') {
      if (codIntroduc == codCorect) {
        lcd.print("Cod valid");
        ledVerde.on();
        ledRosu.off();
      } else {
        lcd.print("Cod invalid");
        ledRosu.on();
        ledVerde.off();
      }
      delay(2000);
      codIntroduc = "";
      lcd.setCursor(0, 0);
      lcd.print("Introduceti cod:");
    } else if (customKey == '*') {
      codIntroduc = "";
      lcd.setCursor(0, 1);
      lcd.print("                ");
    } else {
      codIntroduc += customKey;
      lcd.print(customKey);
    }
  }
}

// void lab1() {
//   printf("Enter your command: ");
//   char* input = IO::input();

//   if (strcmp(input, "led on") == 0) {
//       led.on();
//   } else if (strcmp(input, "led off") == 0) {
//       led.off();
//   }
//   printf("\n");
// }