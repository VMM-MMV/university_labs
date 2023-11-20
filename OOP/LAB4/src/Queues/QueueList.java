package Queues;

import java.util.ArrayList;
import java.util.List;

public class QueueList<E> implements Queue<E> {
    private Node<E> head = null;
    private Node<E> tail = null;
    private int len = 0;
    private int size;

    QueueList(int size) {
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
    public void enqueue(E data) {
        if (isFull()) throw new IndexOutOfBoundsException("The Queues.Queue Is Full");

        Node<E> newNode = new Node<>(data);

        if (tail == null) {
            head = tail = newNode;
        } else {
            tail.next = newNode;
            tail = newNode;
        }
        len++;
    }

    @Override
    public E dequeue() {
        if (isEmpty()) throw new IndexOutOfBoundsException("The Queues.Queue Is Empty");

        E temp = head.data;
        head = head.next;
        return temp;
    }

    @Override
    public E peek() {
        return head.data;
    }

    @Override
    public E rear() {
        return tail.data;
    }

    @Override
    public boolean isFull() {
        return len >= size;
    }

    @Override
    public boolean isEmpty() {
        return len <= 0;
    }

    @Override
    public int getLen() {
        return len;
    }

    @Override
    public List<String> toStrings() {
        List<String> tempList = new ArrayList<>();
        while (head != null) {
            tempList.add(head.data.toString());
            head = head.next;
        }
        return tempList;
    }
}
