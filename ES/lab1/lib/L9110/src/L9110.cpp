#include "L9110.h"

// Constructor with pin assignments
MotorControl::MotorControl(uint8_t pinIn1, uint8_t pinIn2) : 
    _pinIn1(pinIn1), 
    _pinIn2(pinIn2), 
    _currentPower(0) {
}

// Convert percentage (-100 to 100) to PWM value (0 to 255)
uint8_t MotorControl::percentToPWM(int percent) {
    return map(abs(percent), 0, 100, 254, 1);
}

// Initialize motor control pins
void MotorControl::init() {
    pinMode(_pinIn1, OUTPUT);
    pinMode(_pinIn2, OUTPUT);
    
    // Ensure motor is stopped initially
    stop();
}

// Set the power level (-100 to 100)
void MotorControl::setPower(int power) {
    // Constrain power to valid range
    if (power > 100) power = 100;
    if (power < -100) power = -100;
    
    _currentPower = power;
    
    if (power == 0) {
        stop();
    } else {
        uint8_t pwmValue = percentToPWM(power);
        bool forward = (power > 0);
        
        if (forward) {
            digitalWrite(_pinIn1, HIGH);
            analogWrite(_pinIn2, pwmValue);
        } else {
            analogWrite(_pinIn1, pwmValue);
            digitalWrite(_pinIn2, HIGH);
        }
    }
}

// Stop the motor
void MotorControl::stop() {
    digitalWrite(_pinIn1, HIGH);
    digitalWrite(_pinIn2, HIGH);
    _currentPower = 0;
}

// Get current power level
int MotorControl::getPower() {
    return _currentPower;
}