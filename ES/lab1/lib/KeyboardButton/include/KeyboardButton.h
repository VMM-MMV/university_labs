#pragma once

class KeyboardButton {
public:
    KeyboardButton(int pin);
    bool isClicked();
    void setup();
    void setPin(int pin);
private:
    int pin;
};