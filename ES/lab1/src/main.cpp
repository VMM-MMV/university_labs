#include <Arduino.h>
#include "TemperatureReader.h"
#include "IO.h"

#define RELAY_PIN 10
#define TEMP_SENSOR_PIN A0

float setPoint = 25.0;
float hysteresis = 2.0;
float currentTemp = 0.0;
bool relayState = false;

TemperatureReader tempReader(TEMP_SENSOR_PIN);

void initSystem(void);
void updateControl(void);
void updateDisplay(void);
void processCommands(void);

void setup() {
  Serial.begin(9600);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);
  
  printf("Temperature Control System with Hysteresis\n");
  printf("Commands: 'u' - Increase set point, 'd' - Decrease set point\n");
  printf("----------------------------------------\n");
}

void loop() {
  currentTemp = tempReader.readTemperature();
  
  updateControl();
  
  updateDisplay();
  
  processCommands();
  
  delay(500);
}

void updateControl() {
  float lowerThreshold = setPoint - hysteresis;
  float upperThreshold = setPoint + hysteresis;
  
  if (currentTemp < lowerThreshold && !relayState) {
    digitalWrite(RELAY_PIN, HIGH);
    relayState = true;
  } 
  else if (currentTemp > upperThreshold && relayState) {
    digitalWrite(RELAY_PIN, LOW);
    relayState = false;
  }
}

void updateDisplay() {
  printf("Current Temperature: %.1f °C, Set Point: %.1f °C, Relay: %s\n", 
         currentTemp, setPoint, relayState ? "ON" : "OFF");
}

void processCommands() {
  if (Serial.available() > 0) {
    char command;
    scanf(" %c", &command);

    switch (command) {
      case 'u':
      case 'U':
        setPoint += 1;
        printf("Set point increased to: %.1f\n", setPoint);
        break;
        
      case 'd':
      case 'D':
        setPoint -= 1;
        printf("Set point decreased to: %.1f\n", setPoint);
        break;
        
      default:
        printf("Unknown command: %c\n", command);
        break;
    }
  }
}