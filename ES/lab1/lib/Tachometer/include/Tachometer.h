#ifndef TACHOMETER_H
#define TACHOMETER_H

#include <Arduino.h>

class Tachometer {
  private:
    static int _tachoPin;
    static volatile unsigned long _pulseCount;
    
    // Private constructor to prevent instantiation
    Tachometer() {}
    
    // Static callback function for the interrupt
    static void _countPulse();
    
  public:
    // Initialize the tachometer with specified pin
    static void begin(int tachoPin);
    
    // Get RPM reading
    static unsigned long getRPM();
};

#endif