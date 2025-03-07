#include "TimerTask.h"

TimerTask::TimerTask(Led& led1, Led& led2, KeypadWrapper& keypad) :
  led1(led1),
  led2(led2),
  keypad(keypad),
  task1(SYSTEM_TICK * 1, SYSTEM_TICK * 0.10),
  task2(SYSTEM_TICK * 2, SYSTEM_TICK * 1),
  task3(SYSTEM_TICK * 1, SYSTEM_TICK * 0.10)
{
  recAmount = task2.getRecurrence();
}

void TimerTask::init() {
  task1 = Task(SYSTEM_TICK * 1, SYSTEM_TICK * 0.10);
  task2 = Task(SYSTEM_TICK * 2, SYSTEM_TICK * 1);
  task3 = Task(SYSTEM_TICK * 1, SYSTEM_TICK * 0.10);
  recAmount = task2.getRecurrence();
}

void TimerTask::execute() {
  char key = keypad.getKey();
  
  if(task1.isReady()) {
    if (key == '1') {
      led1.toggle();
    }
  }

  if(task2.isReady()) {
    if (led1.getState() == LOW) {
      led2.blink(10);
    }
  }

  if(task3.isReady()) {
    Serial.println(key);
    if (key == '2') {
      recAmount -= (SYSTEM_TICK/2);
      task2.setRecurrence(recAmount);
    } else if (key == '3') {
      recAmount += (SYSTEM_TICK/2);
      task2.setRecurrence(recAmount);
    }
  }
}