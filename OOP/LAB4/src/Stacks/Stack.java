package Stacks;

import java.util.List;

public interface Stack<E> {
    void push(E data);
    E pop();
    E peek();
    boolean isEmpty();
    boolean isFull();
    int getLen();
    List<String> toStrings();
}
