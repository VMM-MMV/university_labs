import java.util.List;

public interface DoubleStack<E> {
    void push_a(E data);
    void push_b(E data);
    E pop_a();
    E pop_b();
    E peek_a();
    E peek_b();
    boolean isFullA();
    boolean isFullB();
    boolean isEmptyA();
    boolean isEmptyB();
    List<String> toStrings();
}