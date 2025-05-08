#include <Arduino.h>

const int tachoPin = 2;
volatile unsigned long pulseCount = 0;

void countPulse() {
    pulseCount++;
}

void setup() {
    Serial.begin(9600);
    pinMode(tachoPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(tachoPin), countPulse, FALLING);
}

void loop() {
    delay(1000);
    noInterrupts();
    unsigned long count = pulseCount;
    pulseCount = 0;
    interrupts();
    unsigned long rpm = (count * 60) / 2;
    Serial.print("RPM: ");
    Serial.println(rpm);
}