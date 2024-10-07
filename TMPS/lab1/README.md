# Topic: *SOLID Principles*
## Author: *Vieru Mihai*
## Objectives:
1. Study and understand the The SOLID principles.

## Some Theory:
In object-oriented design, the SOLID principles are five design principles that aim to make software designs more understandable, flexible, and maintainable. These principles address different aspects of object-oriented design and help developers create more robust and scalable systems.
The principles are:
* S ingle Responsibility Principle (SRP)
* O pen-Closed Principle (OCP)
* L iskov Substitution Principle (LSP)
* I nterface Segregation Principle (ISP)
* D ependency Inversion Principle (DIP)   

## Main tasks:
1. Choose an OO programming language and a suitable IDE or Editor (No frameworks/libs/engines allowed).
2. Write a program in a language of choice that implements 2 of the SOLID letters.
3. Upload everything to Github.

## ImplementationFor this Lab I decided to use Java, and Implement the First 2 SOLID Principles:
Single Responsibility and Interface Segregation.
For this purpose I created 3 shapes, circle, line and square. I could've created a general interface called Shape, but not all features of this interface are needed for all shapes which will implement this interface. So I created 3 interfaces Areable, Lengthable and Perimeterable, and then the classes just implement the ones needed.

EX:

```class Circle implements Areable, Perimeterable```

```class Line implements Lengthable```

```class Square implements Areable, Perimeterable, Lengthable```

This is a example of interface segregation.

And I implemented single responsabilty, by making sure the shapes have methods only for things they are responsable for. 

## Conclusions
In conclusion, the implementation of the SOLID principles, particularly the Single Responsibility Principle (SRP) and Interface Segregation Principle (ISP), leads to more organized and maintainable code. By applying SRP, each class or module is focused on a single responsibility, making the code easier to understand, test, and modify. In this case, the design ensured that shape classes (e.g., Circle, Line, Square) were responsible only for the attributes and behaviors relevant to their purpose.

Interface Segregation was applied by creating specific interfaces (Areable, Lengthable, Perimeterable), ensuring that each class only implemented the functionality it needed. This approach avoids the pitfalls of bloated interfaces and makes the system more flexible and adaptable for future changes.

Overall, by adhering to these principles, the design achieved better modularity, promoting the ease of future extensions and maintenance, while also minimizing dependencies and reducing complexity.
