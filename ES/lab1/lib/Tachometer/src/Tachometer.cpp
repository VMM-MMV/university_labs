#include "Tachometer.h"

int Tachometer::_tachoPin = 0;
volatile unsigned long Tachometer::_pulseCount = 0;

// Static callback for interrupt
void Tachometer::_countPulse() {
  _pulseCount++;
}

// Initialize tachometer
void Tachometer::begin(int tachoPin) {
  _tachoPin = tachoPin;
  _pulseCount = 0;
  pinMode(_tachoPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(_tachoPin), _countPulse, FALLING);
}

// Get RPM reading
unsigned long Tachometer::getRPM() {
  noInterrupts();
  unsigned long count = _pulseCount;
  _pulseCount = 0;
  interrupts();
  
  // Calculate RPM (pulses per minute divided by 2 pulses per revolution)
  unsigned long rpm = (count * 60) / 2;
  return rpm;
}