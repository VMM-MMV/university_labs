#pragma once

#include <Arduino.h>

class Joystick {
public:
    Joystick(int vrxPin, int vryPin, int thresholdLow = 300, int thresholdHigh = 700);
    void acquireData();
    
private:
    int vrxPin;
    int vryPin;
    int thresholdLow;
    int thresholdHigh;

    String determineDirection(int x, int y);
};