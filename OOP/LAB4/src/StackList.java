import java.util.ArrayList;
import java.util.List;

public class StackList<E> implements Stack<E> {
    Node<E> head;
    int len;
    int size;
    StackList(int size) {
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
        if (isFull()) {
            throw new IndexOutOfBoundsException("Maxim Size Achieved");
        }

        Node<E> newNode = new Node<>(newData);
        newNode.next = head;
        head = newNode;
        len++;
    }

    @Override
    public E pop() {
        if (isNull()) {
            throw new IndexOutOfBoundsException("The Stack Is Empty");
        }

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
    public boolean isNull() {
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
        while (head != null) {
            tempList.add(head.data.toString());
            head = head.next;
        }
        return tempList;
    }
}
