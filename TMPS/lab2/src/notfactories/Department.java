package src.notfactories;

import java.util.List;

public class Department implements Salary {

    private final List<Salary> employees;
    private String name;

    public Department(String name, List<Salary> employees) {
        this.name = name;
        this.employees = employees;
    }

    @Override
    public double calculateSalary() {
        return employees.stream()
                .mapToDouble(Salary::calculateSalary)
                .sum();
    }

    public String getName() {
        return name;
    }
}
