#include "Joystick.h"

Joystick::Joystick(int vrxPin, int vryPin, int thresholdLow, int thresholdHigh)
    : vrxPin(vrxPin), vryPin(vryPin), thresholdLow(thresholdLow), thresholdHigh(thresholdHigh){}

char* Joystick::determineDirection(int x, int y) {
    if (x < thresholdLow && y < thresholdLow) {
        return "North-West";
    } else if (x < thresholdLow && y > thresholdLow && y < thresholdHigh) {
        return "West";
    } else if (x < thresholdLow && y > thresholdHigh) {
        return "South-West";
    } else if (x > thresholdLow && x < thresholdHigh && y < thresholdLow) {
        return "North";
    } else if (x > thresholdLow && x < thresholdHigh && y > thresholdHigh) {
        return "South";
    } else if (x > thresholdHigh && y < thresholdLow) {
        return "North-East";
    } else if (x > thresholdHigh && y > thresholdLow && y < thresholdHigh) {
        return "East";
    } else if (x > thresholdHigh && y > thresholdHigh) {
        return "South-East";
    } else {
        return "Center";
    }
}

int Joystick::getXValue() {
    return analogRead(vrxPin);
}

int Joystick::getYValue() {
    return analogRead(vryPin);
}
