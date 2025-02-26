#pragma once

#include <Keypad.h>

class KeypadWrapper {
private:
  Keypad keypad;

public:
  KeypadWrapper();

  KeypadWrapper(char (*keys)[4], byte* rowPins, byte* colPins, byte rows, byte cols);

  char getKey();
};