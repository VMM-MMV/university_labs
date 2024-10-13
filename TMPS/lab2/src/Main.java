package src;

public class Main {
    public static void main(String[] args) {
        Person person = new Person.Builder("josh", "doe").build();
        Person personb = person.clone();
        System.out.println(person);
        System.out.println(personb);
    }
}
