public interface Stack<E> {
    void push(E data);
    E pop();
    E peek();
    boolean isNull();
    boolean isFull();
    int getLen();
}
