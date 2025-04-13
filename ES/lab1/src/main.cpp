// main.c - Main program for DC motor controller
#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <queue.h>
#include "IO.h"
#include "Motor.h"

// Semaphore for safe access to the motor controller
SemaphoreHandle_t motor_mutex;

#define MOTOR_IN1 5
#define MOTOR_IN2 6

Motor motor(MOTOR_IN1, MOTOR_IN2);

static const int MAX_CMD_LENGTH = 64;

void getInput() {
  char cmd[MAX_CMD_LENGTH] = {0};
  char param[MAX_CMD_LENGTH] = {0};
  int value = 0;
  
  // Read command using IO class
  char* inputStr = IO::input();
  
  if (inputStr == NULL || strlen(inputStr) == 0) {
      return;
  }
  
  // Parse the command string
  if (sscanf(inputStr, "%s %s %d", cmd, param, &value) < 1) {
      printf("Invalid command format\n");
      return;
  }
  
  // Check if it's a motor command
  if (strcmp(cmd, "motor") == 0) {
      // Process motor commands
      if (strcmp(param, "set") == 0) {
          motor.setPower(value);
          printf("Motor power set to: %d\n", value);
      }
      else if (strcmp(param, "stop") == 0) {
          motor.stop();
          printf("Motor stopped\n");
      }
      else if (strcmp(param, "max") == 0) {
          motor.setMaxPower();
          printf("Motor set to maximum power: %d\n", motor.getPower());
      }
      else if (strcmp(param, "inc") == 0) {
          motor.incrementPower();
          printf("Motor power increased to: %d\n", motor.getPower());
      }
      else if (strcmp(param, "dec") == 0) {
          motor.decrementPower();
          printf("Motor power decreased to: %d\n", motor.getPower());
      }
      else {
          printf("Unknown motor command: %s\n", param);
      }
  }
  else {
      printf("Unknown command: %s\n", cmd);
  }
}

// Task to handle commands
void CommandHandlerTask(void *pvParameters) {
  for (;;) {
    if (xSemaphoreTake(motor_mutex, portMAX_DELAY) == pdTRUE) {
      getInput();
      xSemaphoreGive(motor_mutex);
    }
    
    vTaskDelay(50 / portTICK_PERIOD_MS); // 50ms delay
  }
}

void StatusReportTask(void *pvParameters) {
  for (;;) {
    if (xSemaphoreTake(motor_mutex, portMAX_DELAY) == pdTRUE) {
      printf("Status: Direction=%s, Power=%d%%\n", 
              motor.getDirection(), 
              motor.getPower());
      xSemaphoreGive(motor_mutex);
    }
    
    vTaskDelay(2000 / portTICK_PERIOD_MS); // Report every 2 seconds
  }
}

void setup() {
    // Initialize stdio redirection
    IO::init();
    
    // Initialize motor controller
    motor.init();
    
    // Create a mutex for motor access
    motor_mutex = xSemaphoreCreateMutex();
    
    // Create FreeRTOS tasks
    xTaskCreate(
        CommandHandlerTask,     // Task function
        "CommandHandler",       // Task name
        256,                    // Stack size
        NULL,                   // Task parameters
        2,                      // Priority
        NULL                    // Task handle
    );
    
    xTaskCreate(
        StatusReportTask,       // Task function
        "StatusReport",         // Task name 
        256,                    // Stack size
        NULL,                   // Task parameters
        1,                      // Priority (lower than command handler)
        NULL                    // Task handle
    );
    
    // Start the scheduler
    vTaskStartScheduler();
}

void loop() {
    // Empty, everything is handled by FreeRTOS tasks
}