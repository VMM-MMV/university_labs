#include "KeypadWrapper.h"

const byte DEFAULT_ROWS = 4;
const byte DEFAULT_COLS = 4;

char defaultKeys[DEFAULT_ROWS][DEFAULT_COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte defaultRowPins[DEFAULT_ROWS] = {4, 5, 6, 7};
byte defaultColPins[DEFAULT_COLS] = {8, 9, 10, 11};

KeypadWrapper::KeypadWrapper()
  : keypad(Keypad(makeKeymap(defaultKeys), defaultRowPins, defaultColPins, DEFAULT_ROWS, DEFAULT_COLS)) {}

KeypadWrapper::KeypadWrapper(
  char (*keys)[4], 
  byte* rowPins, 
  byte* colPins, 
  byte rows, 
  byte cols)
  : keypad(Keypad(makeKeymap(keys), rowPins, colPins, rows, cols)) {}

char KeypadWrapper::getKey() {
  return keypad.getKey();
}