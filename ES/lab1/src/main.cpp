#include "L9110.h"

#define MOTOR_IN1 5
#define MOTOR_IN2 6

MotorControl motor(MOTOR_IN1, MOTOR_IN2);

void setup() {
  Serial.begin(9600);
  
  motor.init();
}

void loop() {
  motor.setPower(70);
  Serial.print("Power: ");
  Serial.print(motor.getPower());
  
  delay(100);
}