#pragma once

class Button {
public:
    Button(int pin);
    bool isClicked();
    void setup();
private:
    int pin;
};