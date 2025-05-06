#pragma once

#include <Arduino.h>

class MotorControl {
private:
    // Pin definitions
    uint8_t _pinIn1;
    uint8_t _pinIn2;
    
    // Current motor state
    int _currentPower; // Range: -100 to 100
    
    // Convert percentage (-100 to 100) to PWM value (0 to 255)
    uint8_t percentToPWM(int percent);

public:
    // Constructor with pin assignments
    MotorControl(uint8_t pinIn1, uint8_t pinIn2);
    
    // Initialize motor control pins
    void init();
    
    // Set the power level (-100 to 100)
    void setPower(int power);
    
    // Stop the motor
    void stop();
    
    // Get current power level
    int getPower();
    
    // Get current direction as string
    const char* getDirection();
};