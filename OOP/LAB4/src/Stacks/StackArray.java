package Stacks;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StackArray<E> implements Stack<E> {
    private E[] array;
    private int head = 0;
    private int size;

    public StackArray(int size) {
        this.size = size;
        array = (E[]) new Object[size];
    }

    @Override
    public void push(E newData) {
        if (isFull()) throw new IndexOutOfBoundsException("The Stack Is Full");
        array[head++] = newData;
    }

    @Override
    public E pop() {
        if (isEmpty()) throw new IndexOutOfBoundsException("The Stack Is Empty");
        head--;
        E popedValue = array[head];
        array[head] = null;
        return popedValue;
    }

    @Override
    public E peek() {
        return array[head-1];
    }

    @Override
    public boolean isEmpty() {
        return head <= 0;
    }

    @Override
    public boolean isFull() {
        return head >= size;
    }

    @Override
    public int getLen() {
        return array.length;
    }

    @Override
    public List<String> toStrings() {
        return Arrays.stream(array)
                .map(x -> x == null ? "null" : x.toString())
                .collect(Collectors.toList());
    }
}
