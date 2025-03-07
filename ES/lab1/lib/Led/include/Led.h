#pragma once

class Led {
public:
    Led(int pin);

    void on();
    void off();
    void blink(int delayTime);
    void toggle();
    bool getState();

protected:
    int pin;
    int state;
};