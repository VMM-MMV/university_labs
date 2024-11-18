package Stacks;

import java.util.ArrayList;
import java.util.List;

public class StackList<E> implements Stack<E> {
    Node<E> head;
    int len;
    int size;
    public StackList(int size) {
        this.size = size;
    }

    private static class Node<E> {
        E data;
        Node<E> next;

        Node(E data) {
            this.data = data;
            this.next = null;
        }
    }

    @Override
    public void push(E newData) {
        if (isFull()) throw new IndexOutOfBoundsException("The Stack Is Full");
        Node<E> newNode = new Node<>(newData);
        newNode.next = head;
        head = newNode;
        len++;
    }

    @Override
    public E pop() {
        if (isEmpty()) throw new IndexOutOfBoundsException("The Stack Is Empty");
        E removedHead = head.data;
        head = head.next;
        len--;
        return removedHead;
    }

    @Override
    public E peek() {
        return head.data;
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

    public List<String> toStrings() {
        List<String> tempList = new ArrayList<>();
        Node<E> current = head;
        while (current != null) {
            tempList.add(current.data.toString());
            current = current.next;
        }
        return tempList;
    }
}
