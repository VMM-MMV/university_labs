#include "Task.h"

Task::Task(int offset, int recurrence) {
    this->recurrence = recurrence;
    this->counter = offset;
}

bool Task::isReady() {
    if (--counter <= 0) {
        counter = recurrence;
        return true;
    }
    return false;
}

void Task::setRecurrence(int newRecurrence) {
    recurrence = newRecurrence;
}

int Task::getRecurrence() {
    return recurrence;
}