#pragma once

#include <Arduino.h>

class PhotoResistor {
private:
    uint8_t pin;              // Analog pin the photoresistor is connected to
    float voltRef;            // Reference voltage (typically 5.0V or 3.3V)
    float adcResolution;      // ADC resolution (typically 1023 for 10-bit ADC)
    
    // Calibration parameters
    float minVolt;
    float maxVolt;
    float minLux;
    float maxLux;

public:
    // Constructor
    PhotoResistor(uint8_t pin, float voltRef = 5.0, float adcResolution = 1023.0,
                 float minVolt = 0.0, float maxVolt = 5.0,
                 float minLux = 0, float maxLux = 1000);
    
    // Methods
    void begin();                              // Initialize the sensor
    uint16_t readRawValue();                   // Read raw ADC value
    float convertADCToVoltage(uint16_t adcValue); // Convert ADC to voltage
    float convertVoltageToLux(float voltage);  // Convert voltage to lux (light intensity)
    float readLux();                           // Read and convert to lux in one step
};