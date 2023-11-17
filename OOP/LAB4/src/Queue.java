public interface Queue<E> {
    void enqueue(E data);
    E dequeue();
    boolean isFull();
    boolean isEmpty();
}
