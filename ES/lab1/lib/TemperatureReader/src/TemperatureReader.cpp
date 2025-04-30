#include "TemperatureReader.h"
#include <math.h>

TemperatureReader::TemperatureReader(int sensorPin) {
    pin = sensorPin;
    pinMode(pin, INPUT);
}

float TemperatureReader::readTemperature() {
    const float BETA = 3950; // Beta coefficient
    int analogValue = analogRead(pin);
    float celsius = 1 / (log(1 / (1023.0 / analogValue - 1)) / BETA + 1.0 / 298.15) - 273.15;
    return celsius;
}