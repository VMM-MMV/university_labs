package src;

public class Main {
    public static void main(String[] args) {
        Person person = new Person.Builder("josh", "doe").build();
        System.out.println(person);
    }
}
