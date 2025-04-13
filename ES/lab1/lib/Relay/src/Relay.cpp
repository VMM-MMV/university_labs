#include "Relay.h"

Relay::Relay(int relayPin) {
  pin = relayPin;
  state = false;
}

void Relay::init() {
  pinMode(pin, OUTPUT);
  digitalWrite(pin, LOW);
}

void Relay::on() {
  digitalWrite(pin, HIGH);
  state = true;
}

void Relay::off() {
  digitalWrite(pin, LOW);
  state = false;
}

bool Relay::isOn() {
  return state;
}
