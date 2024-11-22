package src.notfactories.expense;

import java.util.ArrayDeque;
import java.util.Deque;

public class DepartmentIterator implements MyIterator<Salary> {

    private final Deque<Salary> departments;

    public DepartmentIterator(Department department) {
        this.departments = new ArrayDeque<>();
        departments.push(department);
    }

    @Override
    public boolean hasNext() {
        return departments.peek() != null;
    }

    @Override
    public Salary next() {
        Salary salaryHolder = departments.poll();
        if (salaryHolder instanceof Department currDepartment) {
            departments.addAll(currDepartment.salaryHolders());
        }
        return salaryHolder;
    }
}
