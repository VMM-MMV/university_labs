package Stacks.Double;

import Stacks.Double.DoubleStack;

import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class StackDouble<E> implements DoubleStack<E> {
    int size = 5;
    E[] array = (E[]) new Object[size];
    int head_a = -1;
    int head_b = size;

    @Override
    public void push_a(E data) {
        if (conflict()) throw new IllegalStateException("The Stacks Are Colliding");
        array[++head_a] = data;
    }

    @Override
    public void push_b(E data) {
        if (conflict()) throw new IllegalStateException("The Stacks Are Colliding");
        array[--head_b] = data;
    }

    @Override
    public E pop_a() {
        if (isEmptyA()) throw new IndexOutOfBoundsException("Stacks.Stack A is Empty");
        E temp = array[head_a];
        array[head_a--] = null;
        return temp;
    }

    @Override
    public E pop_b() {
        if (isEmptyB()) throw new IndexOutOfBoundsException("Stacks.Stack B is Empty");
        E temp = array[head_b];
        array[head_b++] = null;
        return temp;
    }

    @Override
    public E peek_a() {
        if (isEmptyA()) return null;
        return array[head_a];
    }

    @Override
    public E peek_b() {
        if (isEmptyB()) return null;
        return array[head_b];
    }

    @Override
    public boolean isFullA() {
        return head_a + 1 == head_b;
    }

    @Override
    public boolean isFullB() {
        return head_b - 1 == head_a;
    }

    @Override
    public boolean isEmptyA() {
        return head_a == -1;
    }

    @Override
    public boolean isEmptyB() {
        return head_b == size;
    }

    public boolean conflict() {
        return head_a + 1 == head_b;
    }

    @Override
    public List<String> toStrings() {
        return Arrays.stream(array)
                .map(x -> x == null ? "null" : x.toString())
                .collect(Collectors.toList());
    }
}
