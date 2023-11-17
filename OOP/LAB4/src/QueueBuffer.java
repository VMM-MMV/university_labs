import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class QueueBuffer<E> implements Queue<E> {
    private int size;
    private E[] array;
    private int head;
    private int tail;
    private int len;

    QueueBuffer(int size) {
        this.size = size;
        array = (E[]) new Object[size];
    }

    @Override
    public void enqueue(E data) {
        if (isFull()) throw new IndexOutOfBoundsException("The Queue Is Full");
        array[tail%size] = data;
        tail++;
        len++;
    }

    @Override
    public E dequeue() {
        if (isEmpty()) throw new IndexOutOfBoundsException("The Queue Is Empty");
        E temp = array[head%size];
        array[head%size] = null;
        head++;
        len--;

        return temp;
    }

    @Override
    public boolean isFull() {
        return len == size;
    }

    @Override
    public boolean isEmpty() {
        return len == 0;
    }

    @Override
    public int getLen() {
        return len;
    }

    @Override
    public E peek() {
        return array[head%size];
    }

    @Override
    public E rear() {
        return array[tail%size];
    }


    @Override
    public List<String> toStrings() {
        return Arrays.stream(array)
                .map(x -> x == null ? "null" : x.toString())
                .collect(Collectors.toList());
    }
}
