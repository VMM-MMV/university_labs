package src.notfactories;

public class Main {
    public static void main(String[] args) {
        Person person = new Person.Builder("josh", "doe").address("myHome").build();
        Person personb = person.copy();
        System.out.println(person);
        System.out.println(personb);

        PersonObjectPool resourcePool = PersonObjectPool.getInstance(3);

        Person person1 = resourcePool.borrowObject();
        person1.setFirstName("Resource 1");
        person1.setLastName("Damn");
        System.out.println("Borrowed: " + person1);

        Person person2 = resourcePool.borrowObject();
        person2.setFirstName("Resource 1");
        person2.setLastName("Damn");
        System.out.println("Borrowed: " + person2);

        resourcePool.returnObject(person1);
        resourcePool.returnObject(person2);

        Person person3 = resourcePool.borrowObject();
        System.out.println("Reused: " + person3);

        resourcePool.returnObject(person3);
    }
}