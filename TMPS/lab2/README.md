# Topic: *Creational Design Patterns*
## Author: *Drumea Vasile*
------
## Objectives:
__1. Study and understand the Creational Design Patterns.__

__2. Choose a domain, define its main classes/models/entities and choose the appropriate instantiation mechanisms.__

__3. Use some creational design patterns for object instantiation in a sample project.__

## Some Theory:
In software engineering, the creational design patterns are the general solutions that deal with object creation, trying to create objects in a manner suitable to the situation. The basic form of object creation could result in design problems or added complexity to the design. Creational design patterns solve this problem by optimizing, hiding or controlling the object creation.

Some examples of this kind of design patterns are:

   * Singleton
   * Builder
   * Prototype
   * Object Pooling
   * Factory Method
   * Abstract Factory
   
## Main tasks:
__1. Choose an OO programming language and a suitable IDE or Editor (No frameworks/libs/engines allowed).__

__2. Select a domain area for the sample project.__

__3. Define the main involved classes and think about what instantiation mechanisms are needed.__

__4. Based on the previous point, implement atleast 3 creational design patterns in your project.__

## Solution:

#### Singleton:
I implemented the singleton patterns for the PesonObjectPool:


```java
public static PersonObjectPool<Person> getInstance(int maxPoolSize) {
    if (instance == null) {
        lock.lock();
        try {
            if (instance == null) {
                instance = new PersonObjectPool<>(maxPoolSize, Person::new);
            }
        } finally {
            lock.unlock();
        }
    }
    return instance;
}
```

I have a variable for the instance and I check if it's null. If yes, then we have never created a instance of the singleton. 

Then we lock the method for one thread using Reantrant lock for multithreaded access to the method. We then check again after locking, for the case where 2 threads passed the first check. There are 2 checks so that we don't lock the thread everytime we need a new instance of the PersonObjectPool. Then if the instance is null we create a new object and set it to the object instance, if not, return the previous instance.