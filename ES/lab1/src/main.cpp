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


