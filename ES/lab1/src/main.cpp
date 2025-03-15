#include <Arduino_FreeRTOS.h>
#include <semphr.h>
#include <queue.h>
#include <Arduino.h>
#include "Button.h"
#include "Led.h"
#include "IO.h"

// Pins definition
#define BUTTON_PIN 11
#define TASK1_LED_PIN 12
#define TASK2_LED_PIN 13

// Task periods (in milliseconds)
#define TASK1_PERIOD 10
#define TASK2_DELAY 50 
#define TASK3_PERIOD 200
#define LED_ON_TIME 300
#define LED_OFF_TIME 500
#define BUTTON_LED_ON_TIME 1000  // 1 second

#define MAX_BUFFER_SIZE 20

Button button(BUTTON_PIN);
Led task1Led(TASK1_LED_PIN);
Led task2Led(TASK2_LED_PIN);

SemaphoreHandle_t xButtonSemaphore;
QueueHandle_t xDataQueue;
int N = 0;

void TaskButtonLed(void *pvParameters);
void TaskSynchronous(void *pvParameters);
void TaskAsynchronous(void *pvParameters);

void setup() {
  Serial.begin(9600);
  
  while (!Serial) {;}

  IO::init();
  
  button.setup();
  
  // Create binary semaphore for button press
  xButtonSemaphore = xSemaphoreCreateBinary();
  if (xButtonSemaphore == NULL) {
    Serial.println(F("Error creating button semaphore"));
    while (1);  // Stop if semaphore creation failed
  }
  
  // Create queue for data communication
  xDataQueue = xQueueCreate(MAX_BUFFER_SIZE, sizeof(uint8_t));
  if (xDataQueue == NULL) {
    Serial.println(F("Error creating data queue"));
    while (1);  // Stop if queue creation failed
  }
  
  xTaskCreate(TaskButtonLed, "ButtonLed", 128, NULL, 3, NULL);
  
  xTaskCreate(TaskSynchronous, "SyncTask", 128, NULL, 3, NULL);
  
  xTaskCreate(TaskAsynchronous, "AsyncTask", 128, NULL, 3, NULL );  
}

void loop() {}

void TaskButtonLed(void *pvParameters) {
  TickType_t xLastWakeTime;
  
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    if (button.isClicked()){
      // task1Led.on();

      // vTaskDelay(pdMS_TO_TICKS(BUTTON_LED_ON_TIME));

      // task1Led.off();

      task1Led.blink(BUTTON_LED_ON_TIME);
      
      xSemaphoreGive(xButtonSemaphore);   
    }
    
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(TASK1_PERIOD));
  }
}

void TaskSynchronous(void *pvParameters) {
  uint8_t data;
  
  for (;;) {
    if (xSemaphoreTake(xButtonSemaphore, portMAX_DELAY) == pdTRUE) {
      N++;

      vTaskDelay(pdMS_TO_TICKS(TASK2_DELAY));
      for (int i = N; i >= 0; i--) {
        data = i;
        xQueueSendToFront(xDataQueue, &data, portMAX_DELAY);
      }
      
      for (int i = 0; i < N; i++) {
        // LED ON for 300ms
        task2Led.on();
        vTaskDelay(pdMS_TO_TICKS(LED_ON_TIME));
        
        // LED OFF for 500ms
        task2Led.off();
        vTaskDelay(pdMS_TO_TICKS(LED_OFF_TIME));
      }
    }
  }
}

void TaskAsynchronous(void *pvParameters) {
  TickType_t xLastWakeTime;
  uint8_t receivedData;
  bool newLine = true;
  
  xLastWakeTime = xTaskGetTickCount();
  
  for (;;) {
    while (xQueueReceive(xDataQueue, &receivedData, 0) == pdTRUE) {
      if (receivedData == 0) {
        // End of sequence marker, print new line
        printf("\n");
        newLine = true;
      } else {
        if (newLine) {
          printf("Task 3 Data: ");
          newLine = false;
        } else {
          printf(", ");
        }
        printf("%i", receivedData);
      }
    }
    
    // Execute task every 200ms
    vTaskDelayUntil(&xLastWakeTime, pdMS_TO_TICKS(TASK3_PERIOD));
  }
}