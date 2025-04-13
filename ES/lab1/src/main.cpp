#include <Arduino.h>
#include "Relay.h"
#include "IO.h"

const int RELAY_PIN = 2;
Relay relay(RELAY_PIN);

void setup() {
  Serial.begin(9600);

  IO::init();
  relay.init();
}

void loop() {
  printf("Enter your command: ");

  char* input = IO::input();

  if (strcmp(input, "relay on") == 0) {
    relay.on();
  } else if (strcmp(input, "relay off") == 0) {
    relay.off();
  } else {
    printf("Unknown command: %s\n", input);
  }

  printf("Current relay state: %s\n\n", relay.isOn() ? "ON" : "OFF");
}