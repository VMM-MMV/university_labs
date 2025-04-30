#pragma once

#include <Arduino.h>

class TemperatureReader {
private:
    int pin;

public:
    TemperatureReader(int sensorPin);
    float readTemperature();
};