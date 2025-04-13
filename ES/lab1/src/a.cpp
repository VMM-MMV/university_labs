#pragma once

#include <Arduino.h>

class Motor {
private:
    // Motor pins
    uint8_t motor_in1;
    uint8_t motor_in2;
    
    // Current motor state
    int current_power; // Range: -100 to 100

    // Convert percentage (-100 to 100) to PWM value (0 to 255)
    uint8_t percent_to_pwm(int percent);

public:
    // Constructor with pin definitions
    Motor(uint8_t in1, uint8_t in2);

    // Initialize motor control pins
    void init();

    // Set the PWM value directly with direction control
    void setPWMandDirection(uint8_t pwmValue, bool forward);

    // Stop the motor
    void stop();

    // Set motor power as a percentage (-100 to 100)
    void setPower(int power);

    // Set motor to maximum speed in current direction
    void setMaxPower();

    // Increment motor power by 10%
    void incrementPower();

    // Decrement motor power by 10%
    void decrementPower();

    // Get current power level (-100 to 100)
    int getPower();

    // Get current direction as string
    const char* getDirection();
};

#include "Motor.h"

Motor::Motor(uint8_t in1, uint8_t in2) : 
  motor_in1(in1), 
  motor_in2(in2), 
  current_power(0) {
}

// Convert percentage (-100 to 100) to PWM value (0 to 255)
uint8_t Motor::percent_to_pwm(int percent) {
  return map(abs(percent), 0, 100, 254, 1);
}

// Initialize motor control pins
void Motor::init() {
  pinMode(motor_in1, OUTPUT);
  pinMode(motor_in2, OUTPUT);

  // Ensure motor is stopped initially
  digitalWrite(motor_in1, HIGH);
  digitalWrite(motor_in2, HIGH);
  current_power = 0;
}

// Set the PWM value directly with direction control
void Motor::setPWMandDirection(uint8_t pwmValue, bool forward) {
  if(!pwmValue) {
    digitalWrite(motor_in1, HIGH);
    digitalWrite(motor_in2, HIGH);
  }
  else if (forward) {
    digitalWrite(motor_in1, HIGH);
    analogWrite(motor_in2, pwmValue);
  } else {
    analogWrite(motor_in1, pwmValue);
    digitalWrite(motor_in2, HIGH);
  }
}

// Stop the motor
void Motor::stop() {
  digitalWrite(motor_in1, HIGH);
  digitalWrite(motor_in2, HIGH);
  current_power = 0;
}

// Set motor power as a percentage (-100 to 100)
void Motor::setPower(int power) {
  // Constrain power to valid range
  if (power > 100) power = 100;
  if (power < -100) power = -100;
  
  current_power = power;
  
  if (power == 0) {
    stop();
  } else {
    setPWMandDirection(percent_to_pwm(power), (power > 0));
  }
}

// Set motor to maximum speed in current direction
void Motor::setMaxPower() {
  if (current_power > 0) {
    setPower(100);
  } else if (current_power < 0) {
    setPower(-100);
  } else {
    // If current power is 0, default to full forward
    setPower(100);
  }
}

// Increment motor power by 10%
void Motor::incrementPower() {
  setPower(current_power + 10);
}

// Decrement motor power by 10%
void Motor::decrementPower() {
  setPower(current_power - 10);
}

// Get current power level (-100 to 100)
int Motor::getPower() {
  return current_power;
}

// Get current direction as string
const char* Motor::getDirection() {
  if (current_power > 0) return "forward";
  if (current_power < 0) return "reverse";
  return "stopped";
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
#include <stdIO.h>
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