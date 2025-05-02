#include <stdlib.h>
#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include "TemperatureReader.h"
#include "Relay.h"
#include "IO.h"

// Pin definitions
#define RELAY_PIN 10
#define TEMP_SENSOR_PIN A0

// Global variables
double setPoint = 200.0;
float hysteresis = 10.0;
float currentTemp = 0.0;

// Create objects
TemperatureReader tempReader(TEMP_SENSOR_PIN);
Relay relay(RELAY_PIN);

// Task handles
TaskHandle_t tempSensorTaskHandle = NULL;
TaskHandle_t controlTaskHandle = NULL;
TaskHandle_t displayTaskHandle = NULL;
TaskHandle_t commandTaskHandle = NULL;

// Task function prototypes
void tempSensorTask(void *pvParameters);
void controlTask(void *pvParameters);
void displayTask(void *pvParameters);
void commandTask(void *pvParameters);

void setup() {
  Serial.begin(9600);
  while(!Serial) {;} // Wait for serial to connect
  
  // Initialize printf redirection
  IO::init();

  // Initialize relay
  relay.init();
  
  // Create FreeRTOS tasks
  xTaskCreate(
    tempSensorTask,         // Task function
    "TempSensor",           // Task name
    128,                    // Stack size
    NULL,                   // Parameters
    3,                      // Priority
    &tempSensorTaskHandle   // Task handle
  );
  
  xTaskCreate(
    controlTask,            // Task function
    "Control",              // Task name
    128,                    // Stack size
    NULL,                   // Parameters 
    3,                      // Priority
    &controlTaskHandle      // Task handle
  );
  
  xTaskCreate(
    displayTask,            // Task function
    "Display",              // Task name
    192,                    // Stack size
    NULL,                   // Parameters 
    2,                      // Priority
    &displayTaskHandle      // Task handle
  );
  
  xTaskCreate(
    commandTask,            // Task function
    "Command",              // Task name
    128,                    // Stack size
    NULL,                   // Parameters 
    1,                      // Priority
    &commandTaskHandle      // Task handle
  );
}

void loop() {
  // Empty, as FreeRTOS tasks handle everything
}

void tempSensorTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(200); // Read temperature every 200ms
  
  // Initialize the xLastWakeTime variable with the current time
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    // Read temperature from sensor
    currentTemp = tempReader.readTemperature();
    
    // Wait for the next cycle using vTaskDelayUntil to ensure constant frequency
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void controlTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(250); // Control logic every 250ms
  
  // Initialize the xLastWakeTime variable with the current time
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    float lowerThreshold = setPoint - hysteresis;
    float upperThreshold = setPoint + hysteresis;
    
    if (currentTemp < lowerThreshold && !relay.isOn()) {
      relay.on();
    } 
    else if (currentTemp > upperThreshold && relay.isOn()) {
      relay.off();
    }
    
    // Wait for the next cycle
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void displayTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(1000); // Update display every 1 second
  
  // Initialize the xLastWakeTime variable with the current time
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    // Display system status
    char currentTempStr[10];
    char setPointStr[10];
    
    dtostrf(currentTemp, 4, 1, currentTempStr);  // width 4, 1 decimal place
    dtostrf(setPoint, 4, 1, setPointStr);        // width 4, 1 decimal place
    
    printf("Current Temperature: %s °C, Set Point: %s °C, Relay: %s\n", 
           currentTempStr, setPointStr, relay.isOn() ? "ON" : "OFF");

    if (currentTemp < 0) {
      printf("It is cold\n");
    }
    
    // Wait for the next cycle
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void commandTask(void *pvParameters) {
  for (;;) {
    if (Serial.available() > 0) {
      char command = Serial.read();

      switch (command) {
        case 'u':
        case 'U':
          setPoint += 1.0;
          break;
          
        case 'd':
        case 'D':
          setPoint -= 1.0;
          break;
          
        default:
          break;
      }
    }
    
    // Small delay to prevent task from consuming too much CPU
    vTaskDelay(pdMS_TO_TICKS(50));
  }
}