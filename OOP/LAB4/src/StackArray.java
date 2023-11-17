import java.util.Arrays;

public class StackArray<E> implements Stack<E> {
    E[] array = (E[]) new Object[5];
    int head = 0;
    @Override
    public void push(E newData) {
        if (isFull()) {
            throw new IndexOutOfBoundsException("Maxim Size Achieved");
        }

        array[head] = newData;
        head++;
    }

    @Override
    public E pop() {
        if (isNull()) {
            throw new IndexOutOfBoundsException("The Stack Is Empty");
        }

        head--;
        E popedValue = array[head];
        array[head] = null;
        return popedValue;
    }

    @Override
    public E peek() {
        return array[head-1];
    }
    @Override
    public boolean isNull() {
        return head <= 0;
    }
    @Override
    public boolean isFull() {
        return head >= 5;
    }

    public void print() {
        System.out.println(Arrays.toString(array));
    }
}
