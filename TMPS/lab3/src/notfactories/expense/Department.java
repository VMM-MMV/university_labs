package src.notfactories.expense;

import java.util.List;

public record Department(String name, List<Salary> salaryHolders) implements Salary {

    @Override
    public double calculateSalary() {
        return salaryHolders.stream()
                .mapToDouble(Salary::calculateSalary)
                .sum();
    }

    public MyIterator<Salary> iterator() {
        return new DepartmentIterator(this);
    }

    @Override
    public String toString() {
        return "Department: " + name + " | Number of Employees: " + salaryHolders.size();
    }
}
