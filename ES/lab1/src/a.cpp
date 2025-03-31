#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <stdio.h>
#include "PhotoResistor.h"
#include "SignalFilter.h"
#include "IO.h"

// Pin definitions
#define PHOTORESISTOR_PIN A0

// Task periods (in milliseconds)
#define ACQUISITION_PERIOD 100
#define PROCESSING_PERIOD 200
#define REPORTING_PERIOD 1000

// Filter parameters
#define SALT_PEPPER_WINDOW 5
#define WEIGHTED_AVG_WINDOW 5

// Create class instances
PhotoResistor photoresistor(PHOTORESISTOR_PIN);
SignalFilter signalFilter(SALT_PEPPER_WINDOW, WEIGHTED_AVG_WINDOW);

// Task handles
TaskHandle_t xAcquisitionTask;
TaskHandle_t xProcessingTask;
TaskHandle_t xReportingTask;

// Semaphore handles
SemaphoreHandle_t xRawDataMutex;
SemaphoreHandle_t xProcessedDataMutex;

// Data structures
typedef struct {
  uint16_t rawADC;
  float voltage;
} RawData_t;

typedef struct {
  float saltPepperFiltered;
  float weightedAvgFiltered;
  float lux;
} ProcessedData_t;

// Shared data
RawData_t xRawData = {0, 0.0};
ProcessedData_t xProcessedData = {0.0, 0.0, 0.0};

// Function prototypes
void vAcquisitionTask(void *pvParameters);
void vProcessingTask(void *pvParameters);
void vReportingTask(void *pvParameters);
void vPrintData(void);

void setup() {
  // Initialize serial communication
  Serial.begin(9600);
  while(!Serial) {;}

  IO::init();
  
  // printf("Photoresistor Signal Processing with FreeRTOS\n");
  // printf("--------------------------------------------\n");
  
  // Initialize our objects
  photoresistor.begin();
  signalFilter.begin();
  
  // Set custom weights for weighted average filter (optional)
  float customWeights[WEIGHTED_AVG_WINDOW] = {0.1, 0.15, 0.2, 0.25, 0.3};
  signalFilter.setWeights(customWeights, WEIGHTED_AVG_WINDOW);
  
  // Create semaphores
  xRawDataMutex = xSemaphoreCreateMutex();
  xProcessedDataMutex = xSemaphoreCreateMutex();
  
  if (xRawDataMutex == NULL || xProcessedDataMutex == NULL) {
    Serial.println(F("Error: Failed to create semaphores"));
    while (1); // Halt execution
  }
  
  // Create tasks
  xTaskCreate(
    vAcquisitionTask,           // Task function
    "Acquisition",              // Task name
    128,                        // Stack size
    NULL,                       // Parameters
    3,                          // Priority (highest)
    &xAcquisitionTask           // Task handle
  );
  
  xTaskCreate(
    vProcessingTask,            // Task function
    "Processing",               // Task name
    256,                        // Stack size
    NULL,                       // Parameters
    2,                          // Priority (medium)
    &xProcessingTask            // Task handle
  );
  
  xTaskCreate(
    vReportingTask,             // Task function
    "Reporting",                // Task name
    256,                        // Stack size
    NULL,                       // Parameters 
    1,                          // Priority (lowest)
    &xReportingTask             // Task handle
  );
  
  // Start the scheduler
  vTaskStartScheduler();
}

void loop() {
  // Empty, as FreeRTOS takes over control
}

// Task for acquiring sensor data
void vAcquisitionTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  xLastWakeTime = xTaskGetTickCount();
  
  while (1) {
    // Read raw ADC value
    uint16_t rawValue = photoresistor.readRawValue();
    float voltage = photoresistor.convertADCToVoltage(rawValue);
    
    // Update shared data with mutex protection
    if (xSemaphoreTake(xRawDataMutex, portMAX_DELAY) == pdTRUE) {
      xRawData.rawADC = rawValue;
      xRawData.voltage = voltage;
      xSemaphoreGive(xRawDataMutex);
    }
    
    // Execute task periodically
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(ACQUISITION_PERIOD));
  }
}

// Task for processing the acquired data
void vProcessingTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  
  // Add offset to stagger task execution
  vTaskDelay(pdMS_TO_TICKS(20));
  xLastWakeTime = xTaskGetTickCount();
  
  while (1) {
    uint16_t rawADC = 0;
    float voltage = 0.0;
    
    // Get raw data with mutex protection
    if (xSemaphoreTake(xRawDataMutex, portMAX_DELAY) == pdTRUE) {
      rawADC = xRawData.rawADC;
      voltage = xRawData.voltage;
      xSemaphoreGive(xRawDataMutex);
    }
    
    // Apply signal conditioning
    float saltPepperFiltered = signalFilter.saltPepperFilter(rawADC);
    float voltageFiltered = photoresistor.convertADCToVoltage(saltPepperFiltered);
    float weightedAvgFiltered = signalFilter.weightedAverageFilter(voltageFiltered);
    float lux = photoresistor.convertVoltageToLux(weightedAvgFiltered);
    
    // Update processed data with mutex protection
    if (xSemaphoreTake(xProcessedDataMutex, portMAX_DELAY) == pdTRUE) {
      xProcessedData.saltPepperFiltered = saltPepperFiltered;
      xProcessedData.weightedAvgFiltered = weightedAvgFiltered;
      xProcessedData.lux = lux;
      xSemaphoreGive(xProcessedDataMutex);
    }
    
    // Execute task periodically
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(PROCESSING_PERIOD));
  }
}

// Task for reporting the processed data
void vReportingTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  
  // Add offset to stagger task execution
  vTaskDelay(pdMS_TO_TICKS(50));
  xLastWakeTime = xTaskGetTickCount();
  
  while (1) {
    vPrintData();
    
    // Execute task periodically
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(REPORTING_PERIOD));
  }
}

// Print all data to serial
void vPrintData() {
  uint16_t rawADC;
  float voltage;
  float saltPepperFiltered;
  float weightedAvgFiltered;
  float lux;
  
  // Get raw data with mutex protection
  if (xSemaphoreTake(xRawDataMutex, portMAX_DELAY) == pdTRUE) {
    rawADC = xRawData.rawADC;
    voltage = xRawData.voltage;
    xSemaphoreGive(xRawDataMutex);
  }
  
  // Get processed data with mutex protection
  if (xSemaphoreTake(xProcessedDataMutex, portMAX_DELAY) == pdTRUE) {
    saltPepperFiltered = xProcessedData.saltPepperFiltered;
    weightedAvgFiltered = xProcessedData.weightedAvgFiltered;
    lux = xProcessedData.lux;
    xSemaphoreGive(xProcessedDataMutex);
  }
  
  printf("--------- Photoresistor Readings ---------\n");
  printf("Raw ADC Value: %d\n", rawADC);
  printf("Voltage: %.2f V\n", voltage);
  printf("Salt & Pepper Filtered: %d\n", saltPepperFiltered);
  printf("Weighted Average Filtered: %.2f V\n", weightedAvgFiltered);
  printf("Light Intensity: %.1f lux\n", lux);
  printf("------------------------------------------\n");
}

#ifndef PHOTORESISTOR_H
#define PHOTORESISTOR_H

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

#endif // PHOTORESISTOR_H

#include "PhotoResistor.h"

PhotoResistor::PhotoResistor(uint8_t _pin, float _voltRef, float _adcResolution,
                           float _minVolt, float _maxVolt, float _minLux, float _maxLux) {
    pin = _pin;
    voltRef = _voltRef;
    adcResolution = _adcResolution;
    minVolt = _minVolt;
    maxVolt = _maxVolt;
    minLux = _minLux;
    maxLux = _maxLux;
}

void PhotoResistor::begin() {
  pinMode(pin, INPUT);
}

uint16_t PhotoResistor::readRawValue() {
  return analogRead(pin);
}

float PhotoResistor::convertADCToVoltage(uint16_t adcValue) {
  return (adcValue / adcResolution) * voltRef;
}

float PhotoResistor::convertVoltageToLux(float voltage) {
  float lux = (voltage - minVolt) * (maxLux - minLux) / (maxVolt - minVolt) + minLux;
  
  // Apply saturation
  if (lux < minLux) {
    lux = minLux;
  } else if (lux > maxLux) {
      lux = maxLux;
  }
  
  return lux;
}

float PhotoResistor::readLux() {
  uint16_t rawValue = readRawValue();
  float voltage = convertADCToVoltage(rawValue);
  return convertVoltageToLux(voltage);
}

#ifndef SIGNAL_FILTER_H
#define SIGNAL_FILTER_H

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

#endif

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
        weights[i] = weights[i];
        sum += weights[i];
    }
    
    // Normalize weights if they don't sum to 1.0
    if (abs(sum - 1.0) > 0.001) {
        for (uint8_t i = 0; i < waWindowSize; i++) {
            weights[i] /= sum;
        }
    }
}

#pragma once

#include <Arduino.h>
#include <stdio.h>

class IO {
public:
    static char* input();
    static void init();
    static void trim(char *str);
    
private:
    static int serial_putchar(char c, FILE* f);
    static int serial_getchar(FILE* f);
};

#include "IO.h"
// #include <stdIO.h>
#include <string.h>
#include <ctype.h>
#include <Arduino.h>

#define MAX_INPUT 100

int IO::serial_putchar(char c, FILE* f) {
    Serial.write(c);
    return 0;
}

int IO::serial_getchar(FILE* f) {
  while (Serial.available() <= 0);
  return Serial.read();
}

void IO::init() {
  FILE* serial_stream = fdevopen(&serial_putchar, &serial_getchar);
  stdin = stdout = serial_stream;
}

void IO::trim(char* str) {
    int i = strlen(str) - 1;
    while (i >= 0 && isspace((unsigned char)str[i])) {
        str[i--] = '\0';
    }

    char *start = str;
    while (isspace((unsigned char)*start)) {
        start++;
    }
    memmove(str, start, strlen(start) + 1);
}

char* IO::input() {
    static char input[MAX_INPUT];
    if (input == NULL) {
        return NULL;
    }

    char c = 0;
    int i = 0;

    while (scanf("%c", &c) != EOF && c != '\n' && i < 99) {
        if (c == '\b' && i > 0) {
            printf("\b \b");
            i--;
        } else if (c != '\b') {
            printf("%c", c);
            input[i++] = c;
        }
    }
    
    input[i] = '\0';
    trim(input);
    return input;
}