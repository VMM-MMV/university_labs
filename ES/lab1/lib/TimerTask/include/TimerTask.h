#pragma once

#include <Arduino.h>
#include "Led.h"
#include "KeypadWrapper.h"

#define SYSTEM_TICK 50

class Task {
private:
  int offset;
  int recurrence;
  int counter;

public:
  Task(int offset, int recurrence) {
    this->offset = offset;
    this->recurrence = recurrence;
    this->counter = offset;
  }

  bool isReady() {
    if(--counter <= 0) {
      counter = recurrence;
      return true;
    }
    return false;
  }

  void setRecurrence(int newRecurrence) {
    recurrence = newRecurrence;
  }

  int getRecurrence() {
    return recurrence;
  }
};

class TimerTask {
private:
  Led& led1;
  Led& led2;
  KeypadWrapper& keypad;
  
  Task task1;
  Task task2;
  Task task3;
  
  int recAmount;

public:
  TimerTask(Led& led1, Led& led2, KeypadWrapper& keypad);
  void init();
  void execute();
};