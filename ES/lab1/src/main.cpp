#include <Arduino.h>
#include "Button.h"
#include "Led.h"
#include "IO.h"
#include <stdio.h>
#include "timer-api.h"
#include "TimerTask.h"

#include "KeypadWrapper.h"

// KeypadWrapper keypad;

// // Button button1(2);
// // Button button2(3);
// // Button button3(4);

// Led led1(13);
// Led led2(12);

// #define SYSTEM_TICK 50

// #define TASK1_OFFSET SYSTEM_TICK * 1
// #define TASK1_REC SYSTEM_TICK * 0.10
// int task1_rec = TASK1_OFFSET;

// #define TASK2_OFFSET SYSTEM_TICK * 2
// #define TASK2_REC SYSTEM_TICK * 1
// int task2_rec = TASK2_OFFSET;
// int REC_AMOUNT = TASK2_REC;

// #define TASK3_OFFSET SYSTEM_TICK * 1
// #define TASK3_REC SYSTEM_TICK * 0.10
// int task3_rec = TASK3_OFFSET;

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

// void setup() {
//   Serial.begin(9600);

//   isr_setup();

//   task1_rec = TASK1_OFFSET;
//   task2_rec = TASK2_OFFSET;
//   REC_AMOUNT = TASK2_REC;
//   task3_rec = TASK3_OFFSET;

//   // button1.setup();
//   // button2.setup();
//   // button3.setup();
// }

// void loop() {
//   Serial.println("Hello from loop!");
//   delay(5000);
// }

// char key;
// /**
//  * Timer interrupt service routine, called with chosen period
//  * @param timer - timer id
//  */
// /**
//  * Процедура, вызываемая прерыванием по событию таймера с заданным периодом
//  * @param timer - идентификатор таймера
//  */
// void timer_handle_interrupts(int timer) {
//   // static unsigned long prev_time = 0;

//   // unsigned long _time = micros();
//   // unsigned long _period = _time - prev_time;
//   // prev_time = _time;

//   key = keypad.getKey();
//   if(task1_rec-- == 1) {
//     if (key == '1') {
//     // if (button1.isClicked()) {
//       led1.toggle();
//     }
    
//     task1_rec = TASK1_REC;
//   }

//   if(task2_rec-- <= 1) {
//     // if (led1.getState() == LOW) {
//     //   led2.on();
//     // } else {
//     //   led2.off();
//     // }
//     if (led1.getState() == LOW) {
//       led2.blink(10);
//     }
    
//     task2_rec = REC_AMOUNT;
//   }

//   if(task3_rec-- == 1) {
//     Serial.println(key);
//     // if (button2.isClicked()) {
//     if (key == '2') {
//       REC_AMOUNT -= (SYSTEM_TICK/2);
//     } else if (key == '3') {
//     // } else if (button3.isClicked()) {
//       REC_AMOUNT += (SYSTEM_TICK/2);
//     }
    
//     task3_rec = TASK3_REC;
//   }
// }



// Global variables
Led led1(13);
Led led2(12);
KeypadWrapper keypad;
TimerTask timerTasks(led1, led2, keypad);

void setup() {
  Serial.begin(9600);
  isr_setup();
  timerTasks.init();
}

void loop() {
  Serial.println("Hello from loop!");
  delay(5000);
}

/**
 * Timer interrupt service routine, called with chosen period
 * @param timer - timer id
 */
void timer_handle_interrupts(int timer) {
  timerTasks.execute();
}
