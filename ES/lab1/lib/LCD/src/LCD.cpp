#include "LCD.h"

LCD::LCD(uint8_t address, uint8_t columns, uint8_t rows) : lcd(address, columns, rows) {}

void LCD::init() {
  lcd.init();
  lcd.backlight();
}
 
void LCD::print(char message) {
  lcd.print(message);
}

void LCD::clear() {
  lcd.clear();
}

void LCD::setCursor(uint8_t col, uint8_t row) {
  lcd.setCursor(col, row);
}