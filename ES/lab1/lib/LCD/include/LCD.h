#pragma once

#include <LiquidCrystal_I2C.h>

class LCD {
private:
  LiquidCrystal_I2C lcd;

public:
  LCD(uint8_t address = 0x27, uint8_t columns = 16, uint8_t rows = 2);
  void init();
  void print(char message);
  void clear();
  void setCursor(uint8_t col, uint8_t row);
};