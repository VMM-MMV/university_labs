#include "Motor.h"

Motor::Motor(uint8_t in1, uint8_t in2) : 
  motor_in1(in1), 
  motor_in2(in2), 
  current_power(0) {
}

// Convert percentage (-100 to 100) to PWM value (0 to 255)
uint8_t Motor::percent_to_pwm(int percent) {
  return map(abs(percent), 0, 100, 254, 1);
}

// Initialize motor control pins
void Motor::init() {
  pinMode(motor_in1, OUTPUT);
  pinMode(motor_in2, OUTPUT);

  // Ensure motor is stopped initially
  digitalWrite(motor_in1, HIGH);
  digitalWrite(motor_in2, HIGH);
  current_power = 0;
}

// Set the PWM value directly with direction control
void Motor::setPWMandDirection(uint8_t pwmValue, bool forward) {
  if(!pwmValue) {
    digitalWrite(motor_in1, HIGH);
    digitalWrite(motor_in2, HIGH);
  }
  else if (forward) {
    digitalWrite(motor_in1, HIGH);
    analogWrite(motor_in2, pwmValue);
  } else {
    analogWrite(motor_in1, pwmValue);
    digitalWrite(motor_in2, HIGH);
  }
}

// Stop the motor
void Motor::stop() {
  digitalWrite(motor_in1, HIGH);
  digitalWrite(motor_in2, HIGH);
  current_power = 0;
}

// Set motor power as a percentage (-100 to 100)
void Motor::setPower(int power) {
  // Constrain power to valid range
  if (power > 100) power = 100;
  if (power < -100) power = -100;
  
  current_power = power;
  
  if (power == 0) {
    stop();
  } else {
    setPWMandDirection(percent_to_pwm(power), (power > 0));
  }
}

// Set motor to maximum speed in current direction
void Motor::setMaxPower() {
  if (current_power > 0) {
    setPower(100);
  } else if (current_power < 0) {
    setPower(-100);
  } else {
    // If current power is 0, default to full forward
    setPower(100);
  }
}

// Increment motor power by 10%
void Motor::incrementPower() {
  setPower(current_power + 10);
}

// Decrement motor power by 10%
void Motor::decrementPower() {
  setPower(current_power - 10);
}

// Get current power level (-100 to 100)
int Motor::getPower() {
  return current_power;
}

// Get current direction as string
const char* Motor::getDirection() {
  if (current_power > 0) return "forward";
  if (current_power < 0) return "reverse";
  return "stopped";
}