#pragma once

class Task {
private:
    int recurrence;
    int counter;

public:
    Task(int offset, int recurrence);

    bool isReady();
    void setRecurrence(int newRecurrence);
    int getRecurrence();
};
