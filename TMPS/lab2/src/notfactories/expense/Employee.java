package src.notfactories.expense;

import src.notfactories.Person;

public abstract class Employee extends Person implements Salary {

    private final double salary;

    public Employee(String firstName, String lastName, int age, String address, String phone, double salary) {
        super(firstName, lastName, age, address, phone);
        this.salary = salary;
    }

    @Override
    public double calculateSalary() {
        return salary;
    }
}
