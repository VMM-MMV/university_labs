package src.notfactories.expense;

import java.util.List;

public class Department implements Salary {

    private final List<Salary> salaryHolders;
    private final String name;

    public Department(String name, List<Salary> salaryHolders) {
        this.name = name;
        this.salaryHolders = salaryHolders;
    }

    @Override
    public double calculateSalary() {
        return salaryHolders.stream()
                .mapToDouble(Salary::calculateSalary)
                .sum();
    }

    public String getName() {
        return name;
    }
}
