import java.util.List;

public interface Queue<E> {
    void enqueue(E data);
    E dequeue();
    boolean isFull();
    boolean isEmpty();
    int getLen();
    List<String> toStrings();
}
