public class QueueList<E> implements Queue<E> {
    Node<E> head = null;
    Node<E> tail = null;
    int len = 0;

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
        if (isFull()) throw new IndexOutOfBoundsException("The Queue Is Full");;
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
        if (isEmpty()) throw new IndexOutOfBoundsException("The Queue Is Empty");

        E temp = head.data;
        head = head.next;
        return temp;
    }

    @Override
    public boolean isFull() {
        return len >= 5;
    }

    @Override
    public boolean isEmpty() {
        return len <= 0;
    }

    public void print() {
        while (head != null) {
            System.out.println(head.data);
            head = head.next;
        }
    }
}
