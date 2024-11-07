# Topic: *Structural Design Patterns*
## Author: *Vieru Mihai*
------
## Objectives:
&ensp; &ensp; __1. Study and understand the Structural Design Patterns.__

&ensp; &ensp; __2. As a continuation of the previous laboratory work, think about the functionalities that your system will need to provide to the user.__

&ensp; &ensp; __3. Implement some additional functionalities using structural design patterns.__

## Theoretical background:
&ensp; &ensp; In software engineering, the Structural Design Patterns are concerned with how classes and objects are composed to form larger structures. Structural class patterns use inheritance to create a hierarchy of classes/abstractions, but the structural object patterns use composition which is generally a more flexible alternative to inheritance.

&ensp; &ensp; Some examples of from this category of design patterns are:

* Adapter
* Bridge
* Composite
* Decorator
* Facade
* Flyweight
* Proxy

## Implementation:
I chose 3 design patterns: Composite, Bridge, and Facade.


### Composite and Bridge
The implementation is as follows: I have departments within a company, and each department can contain different types of employees (Programmers, Managers, ...). I used the Composite pattern to calculate the total salary expenses in the company.

To do this, I created an interface with a common method, calculateSalary:
```java
@FunctionalInterface
public interface Salary {
    double calculateSalary();
}
```

Next, I created Employee and Department:
```java
public abstract class Employee extends Person implements Salary {}
```
The Employee class directly extends what I implemented in the last lab, concording to the requirements. 

It also implements the Salary interface. So I implement the `calculateSalary` method:
```java
@Override
public double calculateSalary() {
    return salary;
}
```

Same thing for the Department:
```java
public class Department implements Salary {}
```

But here the implementation for the `calculateSalary` is a bit different.

Here I use the Bridge pattern to work on the abstraction of type Salary rather than, its direct implementation.
Which allows us later to add as many Salary implementations as one wants, because we have the bridge to their abstraction:

```java
private final List<Salary> salaryHolders;
```

And now you can just recursively calculate the salary for every employee and department:
```java
@Override
public double calculateSalary() {
    return salaryHolders.stream()
            .mapToDouble(Salary::calculateSalary)
            .sum();
    }
```

The way this works is that when it's a employee, it will just return his salary, but for every sub department it will
calculate the salary for all its internal employees, and then return, but if there is another department inside it will 
do the calculation again inside that one, ad infinitum, until there remain only employees/leaves.


### Facade

For the Facade I just chose the PersonObjectPool implementation. 

Since when you need to get a instance of it, it just
hides its implementation inside. 

So you don't have to worry about making sure there is only one instance, or giving the 
implementation for how to create a object inside the pool. You just call the `getInstance` method, and start using it.

```java
public static PersonObjectPool getInstance(int maxPoolSize) {
    if (instance == null) {
        lock.lock();
        try {
            if (instance == null) {
                instance = new PersonObjectPool(maxPoolSize, Person::new);
            }
        } finally {
            lock.unlock();
        }
    }
    return instance;
}
```

## Conclusion

I used Composite and Bridge patterns to calculate the salary for employees in a company. 
Composite being the main structure adn allowing to add complex internal structures,
and Bridge allowing to easily add new types of employees to that structure.

For the facade I just showcased a place in program where I previously have implemented it to abstract way the details
of the implementation for the PersonObjectPool class.