#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include "Joystick.h"

// Pin definitions
#define VRX_PIN A0 // Analog pin for X-axis
#define VRY_PIN A1 // Analog pin for Y-axis

// Joystick threshold values
#define THRESHOLD_LOW  300
#define THRESHOLD_HIGH 700

// Create objects
Joystick joystick(VRX_PIN, VRY_PIN, THRESHOLD_LOW, THRESHOLD_HIGH);

// Global variables for joystick data
int xValue = 0;
int yValue = 0;
char* direction;

// Task handles
TaskHandle_t acquisitionTaskHandle = NULL;
TaskHandle_t displayTaskHandle = NULL;

// Task functions
void acquisitionTask(void *pvParameters);
void displayTask(void *pvParameters);

// Custom printf function for Serial output
int serial_putchar(char c, FILE* f) {
  Serial.write(c);
  return 0;
}

int serial_getchar(FILE* f) {
  while (Serial.available() <= 0);
  return Serial.read();
}

void initPrintf() {
  static FILE serial_stream;
  fdev_setup_stream(&serial_stream, serial_putchar, serial_getchar, _FDEV_SETUP_WRITE);
  stdout = &serial_stream;
  stdin = &serial_stream;
}

void setup() {
  Serial.begin(9600);
  while(!Serial) {;} // Wait for serial to connect
  
  // Initialize printf redirection
  initPrintf();
  
  printf("Initializing Joystick Control System...\n");
  
  // Create FreeRTOS tasks
  xTaskCreate(
    acquisitionTask,        // Task function
    "Acquisition",          // Task name
    128,                    // Stack size
    NULL,                   // Parameters
    3,                      // Priority
    &acquisitionTaskHandle  // Task handle
  );
  
  xTaskCreate(
    displayTask,            // Task function
    "Display",              // Task name
    256,                    // Stack size (larger for display task)
    NULL,                   // Parameters 
    3,                      // Priority
    &displayTaskHandle      // Task handle
  );
  
  // Print initialization message
  printf("System initialized. Starting tasks...\n\n");
}

void loop() {
  // Empty, as FreeRTOS tasks handle everything
}

void acquisitionTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(50);
  
  // Initialize the xLastWakeTime variable with the current time
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    xValue = joystick.getXValue();
    yValue = joystick.getYValue();
    
    direction = joystick.determineDirection(xValue, yValue);
    
    // Wait for the next cycle
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}

void displayTask(void *pvParameters) {
  TickType_t xLastWakeTime;
  const TickType_t xFrequency = pdMS_TO_TICKS(500);
  
  // Initialize the xLastWakeTime variable with the current time
  xLastWakeTime = xTaskGetTickCount();
  
  char* sequence[] = {"North", "North-East", "East", "South-East", "South", "South-West", "West", "North-West", "North"};
  int sequenceIndex = 0;
  
  for (;;) {
    printf("\n");
    
    // Display system status
    printf("Joystick Data:\n");
    printf("  X-axis: %d ", xValue);
    printf("  Y-axis: %d ", yValue);
    printf("  Direction: %s ", direction);
    
    // Check if the direction matches the current or previous expected value in sequence
    char* prev = 0;
    printf("%i", sequenceIndex);
    if (strcmp(direction, prev) != 0) {
      if (strcmp(direction, sequence[sequenceIndex]) == 0) {
        prev = direction;
        sequenceIndex++;
        
        // If the entire sequence is matched, print the message and reset
        if (sequenceIndex == 9) {
          printf("\nYou have unlocked the message: Around the Globe!\n");
          sequenceIndex = 0;
          prev = 0;
        }
      }
    } else if (strcmp(direction, "Center") != 0) {
      sequenceIndex = 0;
      prev = 0;
    }
    
    printf("\n");
    
    // Wait for the next cycle
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
}