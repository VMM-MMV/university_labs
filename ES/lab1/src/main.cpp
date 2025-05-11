#include <Arduino.h>
#include "Button.h"
#include "Led.h"
#include "IO.h"
#include "State.h"

#define LED_PIN 13
#define BUTTON_PIN 8

#define LED_OFF_STATE LOW
#define LED_ON_STATE HIGH

Button button(BUTTON_PIN);
Led led(LED_PIN);

STm FSM[2] = {
  {LED_OFF_STATE, 100, {LED_OFF_STATE, LED_ON_STATE}},
  {LED_ON_STATE, 100, {LED_ON_STATE, LED_OFF_STATE}}
};

int currentState = LED_OFF_STATE;

void setup() {
  Serial.begin(9600);
  while(!Serial) {;}

  IO::init();
  button.setup();
}

void loop() {
  led.setState(FSM[currentState].ledState);
  
  int input = button.isClickedDB();

  currentState = FSM[currentState].nextState[input];
  printf("Current led state: %i\n", currentState);
  
  delay(FSM[currentState].delayTime);
}
