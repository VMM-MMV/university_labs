public class RunStructures {
    public static void main(String[] args) {
//        QueueList<Object> queueList = new QueueList<>();
//
//        queueList.enqueue("Jora");
//        queueList.enqueue("Vora");
//        System.out.println(queueList.toStrings());
//        StackList<Object> stackList = new StackList<>(5);
//        stackList.push("Jora");
//        stackList.push("Vora");
//        stackList.push(1);
//        System.out.println(stackList.toStrings());
//        StackArray<Object> stackArray = new StackArray<>();
//        stackArray.push(5);
//        stackArray.push("ahahah");
//        System.out.println(stackArray.toStrings());
        QueueBuffer<Object> queueBuffer = new QueueBuffer<>(5);
        queueBuffer.enqueue(1);
        queueBuffer.enqueue(2);
        queueBuffer.enqueue(3);
        queueBuffer.enqueue(4);
        queueBuffer.enqueue(5);
        queueBuffer.dequeue();
        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
//        queueBuffer.dequeue();
        queueBuffer.enqueue(6);
        queueBuffer.enqueue(7);
        System.out.println(queueBuffer.toStrings());
        System.out.println(queueBuffer.peek());
//        System.out.println(queueArray.head);
//        System.out.println(queueArray.tail);
    }
}
