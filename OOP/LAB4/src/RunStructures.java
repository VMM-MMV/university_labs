public class RunStructures {
    public static void main(String[] args) {
        StackList<Object> stackArray = new StackList<>();
        stackArray.push("Hi");
        stackArray.push("Welcome");
        stackArray.push("Hello");
        stackArray.push("Hello2");
        stackArray.pop();
        stackArray.push("Hello3");

        System.out.println(stackArray.len);
        System.out.println(stackArray.peek());
        stackArray.print();
    }
}
