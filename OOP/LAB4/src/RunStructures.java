public class RunStructures {
    public static void main(String[] args) {
//        QueueList<Object> queueList = new QueueList<>(5);
//
//        queueList.enqueue("Jora");
//        queueList.enqueue("Vora");
//        System.out.println(queueList.toStrings());
//        StackList<Object> stackList = new StackList<>(5);
//        stackList.push("Jora");
//        stackList.push("Vora");
//        stackList.push(1);
//        System.out.println(stackList.toStrings());

//        StackArray<Object> stackArray = new StackArray<>(5);
//        stackArray.push(5);
//        stackArray.push("ahahah");
//        stackArray.pop();
//        System.out.println(stackArray.peek());
//        System.out.println(stackArray.toStrings());

//        QueueBuffer<Object> queueBuffer = new QueueBuffer<>(5);
//        queueBuffer.enqueue(1);
//        queueBuffer.enqueue(2);
//        queueBuffer.enqueue(3);
//        queueBuffer.enqueue(4);
//        queueBuffer.enqueue(5);
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.enqueue(6);
//        queueBuffer.enqueue(7);
//        queueBuffer.dequeue();
//        System.out.println(queueBuffer.peek());
//        System.out.println(queueBuffer.rear());
//        System.out.println(queueBuffer.toStrings());


//        QueueArray<Object> queueArray = new QueueArray<>(5);
//        queueArray.enqueue(1);
//        queueArray.enqueue(2);
//        queueArray.enqueue(3);
//        queueArray.dequeue();
//        queueArray.dequeue();
//        System.out.println(queueArray.peek());
//        System.out.println(queueArray.rear());
//        System.out.println(queueArray.toStrings());
//        queueArray.enqueue(4);
//        queueArray.enqueue(5);
//        queueArray.dequeue();
//        System.out.println(queueArray.peek());
//        System.out.println(queueArray.rear());
//        System.out.println(queueArray.toStrings());
//        int[] array = {1,2,3,4,5};
//        System.out.println(array[0]);
//        System.out.println(array[-1]);
//        System.out.println(array);

        StackDouble<Object> stackDouble = new StackDouble<>();
        stackDouble.push_b(1);
        stackDouble.push_b(2);
        stackDouble.push_b(3);
        stackDouble.push_b(4);
        stackDouble.push_b(5);
        System.out.println(stackDouble.pop_b());
        stackDouble.pop_b();
        stackDouble.push_a("F");
        stackDouble.push_a("A");
        System.out.println(stackDouble.pop_a());
//        stackDouble.push_a("F");
        System.out.println(stackDouble.peek_a());
        System.out.println(stackDouble.peek_b());
        System.out.println(stackDouble.toStrings());
    }
}
