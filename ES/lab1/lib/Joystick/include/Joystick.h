#pragma once

#include <Arduino.h>

class Joystick {
public:
    Joystick(int vrxPin, int vryPin, int thresholdLow = 300, int thresholdHigh = 700);
    char* determineDirection(int x, int y);
    int getXValue();
    int getYValue();
    
private:
    int vrxPin;
    int vryPin;
    int thresholdLow;
    int thresholdHigh;

};