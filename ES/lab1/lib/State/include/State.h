#pragma once

struct State {
    int ledState;               // LED ON/OFF
    unsigned long delayTime;    // Delay time in milliseconds
    int nextState[2];           // Next state based on button input: [released, pressed]
};

// Define a type alias for const State
typedef const struct State STm;