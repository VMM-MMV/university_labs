package Queues;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class QueueArray<E> implements Queue<E> {
    private int head = 0;
    private int tail = 0;
    private int size;
    private int len;
    private E[] array;

    QueueArray(int size) {
        this.size = size;
        array = (E[]) new Object[size];
    }
    @Override
    public void enqueue(E data) {
        if (isFull()) throw new IndexOutOfBoundsException("The Queues.Queue Is Full");
        array[tail++] = data;
        len++;
    }

    @Override
    public E dequeue() {
        if (isEmpty()) throw new IndexOutOfBoundsException("The Queues.Queue Is Empty");
        E temp = array[head];
        tail--;
        array = Arrays.copyOfRange(array, head+1, size-head+1);

        return temp;
    }

    @Override
    public E peek() {
        return array[head];
    }

    @Override
    public E rear() {
        return array[tail-1];
    }

    @Override
    public boolean isEmpty() {
        return len <= 0;
    }

    @Override
    public boolean isFull() {
        return len >= size;
    }

    @Override
    public int getLen() {
        return len;
    }

    @Override
    public List<String> toStrings() {
        return Arrays.stream(array)
                .map(x -> x == null ? "null" : x.toString())
                .collect(Collectors.toList());
    }
}
