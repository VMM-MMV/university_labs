// Example usage in Arduino:
//
// #include "SignalFilter.h"
//
// SignalFilter filter(5, 4);  // salt-pepper window size 5, weighted avg window size 4
//
// void setup() {
//     Serial.begin(9600);
//     filter.begin();
// }
//
// void loop() {
//     uint16_t sensorValue = analogRead(A0);  // read analog pin A0
//     float median = filter.saltPepperFilter(sensorValue);
//     float weightedAvg = filter.weightedAverageFilter((float)sensorValue);
//
//     Serial.print("Median: ");
//     Serial.print(median);
//     Serial.print("\tWeighted Avg: ");
//     Serial.println(weightedAvg);
//
//     delay(500);  // wait half a second
// }

#include "SignalFilter.h"

SignalFilter::SignalFilter(uint8_t saltPepperWindowSize, uint8_t weightedAvgWindowSize) {
    spWindowSize = saltPepperWindowSize;
    waWindowSize = weightedAvgWindowSize;
    
    // Allocate memory for buffers
    spBuffer = new uint16_t[spWindowSize];
    waBuffer = new float[waWindowSize];
    weights = new float[waWindowSize];
    
    // Initialize buffer indices
    spBufferIndex = 0;
    waBufferIndex = 0;
    
    // Default weights (linear increasing weights)
    float sum = 0.0;
    for (uint8_t i = 0; i < waWindowSize; i++) {
        weights[i] = (float)(i + 1);
        sum += weights[i];
    }
    
    // Normalize weights to sum to 1.0
    for (uint8_t i = 0; i < waWindowSize; i++) {
        weights[i] /= sum;
    }
}

void SignalFilter::begin() {
    // Initialize buffers to zero
    for (uint8_t i = 0; i < spWindowSize; i++) {
        spBuffer[i] = 0;
    }
    
    for (uint8_t i = 0; i < waWindowSize; i++) {
        waBuffer[i] = 0.0;
    }
}

float SignalFilter::saltPepperFilter(uint16_t newSample) {
    // Update circular buffer
    spBuffer[spBufferIndex] = newSample;
    spBufferIndex = (spBufferIndex + 1) % spWindowSize;
    
    // Create a copy for sorting
    uint16_t sortedBuffer[spWindowSize];
    memcpy(sortedBuffer, spBuffer, sizeof(uint16_t) * spWindowSize);
    
    // Simple bubble sort (efficient for small arrays)
    for (uint8_t i = 0; i < spWindowSize - 1; i++) {
        for (uint8_t j = 0; j < spWindowSize - i - 1; j++) {
            if (sortedBuffer[j] > sortedBuffer[j + 1]) {
                uint16_t temp = sortedBuffer[j];
                sortedBuffer[j] = sortedBuffer[j + 1];
                sortedBuffer[j + 1] = temp;
            }
        }
    }
    
    // Return median value
    return sortedBuffer[spWindowSize / 2];
}

float SignalFilter::weightedAverageFilter(float newSample) {
    // Update circular buffer
    waBuffer[waBufferIndex] = newSample;
    waBufferIndex = (waBufferIndex + 1) % waWindowSize;
    
    // Calculate weighted average
    float sum = 0.0;
    uint8_t bufIdx;
    
    for (uint8_t i = 0; i < waWindowSize; i++) {
        bufIdx = (waBufferIndex + waWindowSize - i - 1) % waWindowSize;
        sum += waBuffer[bufIdx] * weights[i];
    }
    
    return sum;
}

void SignalFilter::setWeights(float* weights, uint8_t size) {
    // Check if size matches window size
    if (size != waWindowSize) {
        return; // Error: size mismatch
    }
    
    // Copy weights
    float sum = 0.0;
    for (uint8_t i = 0; i < waWindowSize; i++) {
        this->weights[i] = weights[i];
        sum += weights[i];
    }
    
    // Normalize weights if they don't sum to 1.0
    if (abs(sum - 1.0) > 0.001) {
        for (uint8_t i = 0; i < waWindowSize; i++) {
            this->weights[i] /= sum;
        }
    }
}
