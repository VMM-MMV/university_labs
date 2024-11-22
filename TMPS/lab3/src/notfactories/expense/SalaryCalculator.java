package src.notfactories.expense;

import java.util.Arrays;

public class SalaryCalculator {
    public static void main(String[] args) {
        Department company = new Department("Company", Arrays.asList(
                new Department("Tech Division", Arrays.asList(
                        new Manager("Alice", "Johnson", 40, "1234 Elm St", "555-1234", 80000),
                        new Programmer("Bob", "Smith", 30, "5678 Oak St", "555-5678", 60000),
                        new Programmer("Charlie", "Brown", 28, "91011 Pine St", "555-9101", 65000)
                )),

                new Department("HR Division", Arrays.asList(
                        new Manager("David", "White", 45, "1213 Maple St", "555-1213", 85000),
                        new Programmer("Eve", "Davis", 25, "1415 Birch St", "555-1415", 55000),

                        new Department("Employee Relations", Arrays.asList(
                                new Manager("Helen", "Clark", 38, "1617 Cedar St", "555-1617", 75000),
                                new Programmer("Frank", "Williams", 32, "1819 Walnut St", "555-1819", 64000),

                                new Department("HR Employee Reaction Training", Arrays.asList(
                                        new Manager("George", "Martin", 50, "2021 Spruce St", "555-2021", 90000),
                                        new Programmer("Ivy", "King", 29, "2223 Fir St", "555-2223", 61000)
                                ))
                        ))
                ))
        ));
        System.out.println(company.getName() + "Salary: " + company.calculateSalary());

        MyIterator<Salary> iterator = company.iterator();
        while (iterator.hasNext()) {
            Salary employee = iterator.next();
            System.out.println(employee);
        }
    }
}
