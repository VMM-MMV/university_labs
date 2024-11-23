package src.notfactories.expense;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

public record Department(String name, List<Salary> salaryHolders) implements Salary {

    private static class DepartmentIterator implements MyIterator<Salary> {

        private final Deque<Salary> salaryHolders;

        public DepartmentIterator(Department department) {
            this.salaryHolders = new ArrayDeque<>();
            salaryHolders.push(department);
        }

        @Override
        public boolean hasNext() {
            return salaryHolders.peek() != null;
        }

        @Override
        public Salary next() {
            Salary salaryHolder = salaryHolders.poll();
            if (salaryHolder instanceof Department currDepartment) {
                salaryHolders.addAll(currDepartment.salaryHolders());
            }
            return salaryHolder;
        }
    }

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
