#pragma once

#include <Arduino.h>

class SignalFilter {
private:
    // Salt and pepper filter properties
    uint8_t spWindowSize;
    uint16_t* spBuffer;
    uint8_t spBufferIndex;
    
    // Weighted average filter properties
    uint8_t waWindowSize;
    float* waBuffer;
    float* weights;
    uint8_t waBufferIndex;

public:
    // Constructor
    SignalFilter(uint8_t saltPepperWindowSize = 5, uint8_t weightedAvgWindowSize = 5);
    
    // Methods
    void begin();
    float saltPepperFilter(uint16_t newSample);   // Median filter for impulse noise
    float weightedAverageFilter(float newSample); // Weighted average filter for smoothing
    
    // Utility methods
    void setWeights(float* weights, uint8_t size);
};