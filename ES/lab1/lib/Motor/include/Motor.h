#pragma once

#include <Arduino.h>

class Motor {
private:
    // Motor pins
    uint8_t motor_in1;
    uint8_t motor_in2;
    
    // Current motor state
    int current_power; // Range: -100 to 100

    // Convert percentage (-100 to 100) to PWM value (0 to 255)
    uint8_t percent_to_pwm(int percent);

public:
    // Constructor with pin definitions
    Motor(uint8_t in1, uint8_t in2);

    // Initialize motor control pins
    void init();

    // Set the PWM value directly with direction control
    void setPWMandDirection(uint8_t pwmValue, bool forward);

    // Stop the motor
    void stop();

    // Set motor power as a percentage (-100 to 100)
    void setPower(int power);

    // Set motor to maximum speed in current direction
    void setMaxPower();

    // Increment motor power by 10%
    void incrementPower();

    // Decrement motor power by 10%
    void decrementPower();

    // Get current power level (-100 to 100)
    int getPower();

    // Get current direction as string
    const char* getDirection();
};