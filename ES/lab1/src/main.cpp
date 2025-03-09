#include <Arduino.h>
#include "Button.h"
#include "Led.h"
#include "IO.h"
#include <stdio.h>
#include "timer-api.h"
#include "Task.h"
#include "KeypadWrapper.h"

void isr_setup() {
  // http://www.robotshop.com/letsmakerobots/arduino-101-timers-and-interrupts
  // 1. CPU frequency 16Mhz for Arduino
  // 2. maximum timer counter value (256 for 8bit, 65536 for 16bit timer)
  // 3. Divide CPU frequency through the choosen prescaler (16000000 / 256 = 62500)
  // 4. Divide result through the desired frequency (62500 / 2Hz = 31250)
  // 5. Verify the result against the maximum timer counter value (31250 < 65536 success).
  //    If fail, choose bigger prescaler.
  
  // Arduino 16МГц
  // Настроим и запустим таймер с периодом 20 миллисекунд (50 срабатываний в секунду == 50Гц):
  // prescaler=1:8, adjustment=40000-1:
  // 16000000/8/50=40000 (50Hz - срабатывает 50 раз в секунду, т.е. каждые 20мс),
  // минус 1, т.к. считаем от нуля.
  // Обработчик прерывания от таймера - функция timer_handle_interrupts 
  // (с заданными настройками будет вызываться каждые 20мс).
  timer_init_ISR(TIMER_DEFAULT, TIMER_PRESCALER_1_8, 40000-1);
}

Button button1(2);
Button button2(3);
Button button3(4);
#define SYSTEM_TICK 50

Led led1(13);
Led led2(12);
KeypadWrapper keypad;
Task task1(SYSTEM_TICK * 1, 1);
Task task2(SYSTEM_TICK * 2, SYSTEM_TICK * 1);
Task task3(SYSTEM_TICK * 1, 1);

void setup() {
  Serial.begin(9600);
  isr_setup();
  IO::init();
}

void loop() {
  printf("Hello from loop!\n");
  delay(5000);
}

bool isButton1Pressed() {
  return button1.isClicked();
  // return keypad.getKey() == '1';
}

bool isButton2Pressed() {
  return button2.isClicked();
  // return keypad.getKey() == '2';
}

bool isButton3Pressed() {
  return button3.isClicked();
  // return keypad.getKey() == '3';
}

void timer_handle_interrupts(int timer) {
  if (task1.isReady() && isButton1Pressed()) {
    led1.toggle();
  }

  bool led1IsOff = led1.getState() == LOW;
  if (task2.isReady() && led1IsOff) {
    led2.blink(10);
  }

  if (task3.isReady()) {
    if (isButton2Pressed()) {
      task2.setRecurrence(task2.getRecurrence() - (SYSTEM_TICK/2));
    } else if (isButton3Pressed()) {
      task2.setRecurrence(task2.getRecurrence() + (SYSTEM_TICK/2));
    }
  }
}