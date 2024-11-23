# Topic: *Behavioral Design Patterns*
## Author: *Vieru Mihai*
------
## Objectives:
&ensp; &ensp; __1. Study and understand the Behavioral Design Patterns.__

&ensp; &ensp; __2. As a continuation of the previous laboratory work, think about what communication between software entities might be involed in your system.__

&ensp; &ensp; __3. Implement some additional functionalities using behavioral design patterns.__

## Theoretical background:
&ensp; &ensp; In software engineering, behavioral design patterns have the purpose of identifying common communication patterns between different software entities. By doing so, these patterns increase flexibility in carrying out this communication.

&ensp; &ensp; Some examples from this category of design patterns are :

* Chain of Responsibility
* Command
* Interpreter
* Iterator
* Mediator
* Observer
* Strategy

## Main tasks :
&ensp; &ensp; __1. By extending your project, implement at least 1 behavioral design pattern in your project:__
* The implemented design pattern should help to perform the tasks involved in your system.
* The behavioral DPs can be integrated into you functionalities alongside the structural ones.
* There should only be one client for the whole system.

&ensp; &ensp; __2. Keep your files grouped (into packages/directories) by their responsibilities (an example project structure):__
* client;
* domain;
* utilities;
* data(if applies);

&ensp; &ensp; __3. Document your work in a separate markdown file according to the requirements presented below (the structure can be extended of course):__
* Topic of the laboratory work.
* Author.
* Introduction/Theory/Motivation.
* Implementation & Explanation (you can include code snippets as well):
    * Indicate the location of the code snippet.
    * Emphasize the main idea and motivate the usage of the pattern.
* Results/Screenshots/Conclusions;

## Implementation :
The pattern I chose is the Iterator pattern.

I started by specifying an Iterator interface:
```java
public interface MyIterator<T> {
    boolean hasNext();
    T next();
}
```

Then I implement the abstraction to expand the Composite pattern in the last lab, the Department class.
```java
private class DepartmentIterator implements MyIterator<Salary> {}
```

I declare a dequeue for the bfs algorithm to traverse the Composite tree
```java
private final Deque<Salary> salaryHolders;
```

And I initialize the dequeue in the constructor
```java
public DepartmentIterator(Department department) {
    this.salaryHolders = new ArrayDeque<>();
    salaryHolders.push(department);
}
```

Then I start by implementing the iterator methods
```java
@Override
public boolean hasNext() {
  return salaryHolders.peek() != null;
}
```
Here I just see if the dequeue is empty or not.

```java
@Override
public Salary next() {
    Salary salaryHolder = salaryHolders.poll();
    if (salaryHolder instanceof Department currDepartment) {
        salaryHolders.addAll(currDepartment.salaryHolders());
    }
    return salaryHolder;
}
```
And here I just take the first element from the front the dequeue and if it's of the department type I add the list of objects extending Salary they have to the end of the dequeue. Then no matter what, I return the element.

And now in the end you can initialize a iterator by using the method `iterator()` in `Departament`
```java
public MyIterator<Salary> iterator() {
    return new DepartmentIterator(this);
}
```

Now we can iterate over the objects of the composite with the iterator
```java
MyIterator<Salary> iterator = company.iterator();
while (iterator.hasNext()) {
    Salary employee = iterator.next();
    System.out.println(employee);
}
```

