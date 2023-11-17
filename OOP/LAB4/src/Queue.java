import java.util.List;

public interface Queue<E> {
    void enqueue(E data);
    E dequeue();
    E peek();
    E rear();
    boolean isEmpty();
    boolean isFull();
    int getLen();
    List<String> toStrings();
}
