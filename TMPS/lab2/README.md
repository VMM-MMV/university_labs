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
I implemented the singleton pattern for the PesonObjectPool:


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

#### Builder:
I have implemented the builder pattern in the Person class:


First we create a private Person contructor.

```java
private Person(Builder builder) {
    this.firstName = builder.firstName;
    this.lastName = builder.lastName;
    this.age = builder.age;
    this.address = builder.address;
    this.phone = builder.phone;
}
```

It is private because we want to instanciate it only if we make it through the Builder class, in the build method:

```java
public Person build() {
    return new Person(this);
}
```

Then we create the internal Builder class in the Person class, with all of the variables Person has:

```java
public static class Builder {
    private final String firstName;
    private final String lastName;
    private int age;
    private String address;
    private String phone;
```

Then we define the variables a instance should definetely have, by declaring them setable only through the Builder constructor

```java
public Builder(String firstName, String lastName) {
    this.firstName = firstName;
    this.lastName = lastName;
}
```

Then we set the setable variables, which are not always required:

```java
public Builder age(int age) {
    this.age = age;
    return this;
}

public Builder address(String address) {
    this.address = address;
    return this;
}

public Builder phone(String phone) {
    this.phone = phone;
    return this;
}
```

Now we can create a Person like this:

```java
Person person = new Person.Builder("josh", "bou").address("myHome").build();
```

### Prototype:

I implemented the prototype by creating a generic interface for the prototype:

```java
public interface Prototype<T> {
    T clone();
}
```

Then in the Person class we override this method, and give it a implementation:

```java
@Override
public Person clone() {
    return new Builder(this.firstName, this.lastName)
                .age(this.age)
                .address(this.address)
                .phone(this.phone)
                .build();
}
```

We can create a full instance only through the Builder, so we create a Builder with all of the variables of the Person class, which creates a exact copy of the object. 

### Object Pooling:

I have implemented the ObjectPooling by creating a PersonObjectPool:

```java
private PersonObjectPool(int maxPoolSize, ObjectFactory<Person> objectFactory) {
    this.maxPoolSize = maxPoolSize;
    this.objectFactory = objectFactory;
    this.pool = new LinkedBlockingQueue<>(maxPoolSize);
}
```

Where maxPoolSize is how many objects max could be in the pool and ObjectFactory is a FunctionalInterface:
```java
@FunctionalInterface
interface ObjectFactory<T> {
    T createObject();
}
```

So now we can create a new instance like this:
```java
new PersonObjectPool<>(maxPoolSize, Person::new);
```

And because ObjectFactory is a functional interface I can create it using the constructor reference for the Person object which implements the
FunctionalInterface method.

But to do this we have to make a empty constructor in the Person class:
```java
public Person() {}
```

Then we implement the borrow and return methods:

```java
public Person borrowObject() {
    Person person = pool.poll();
    if (person == null) {
        person = objectFactory.createObject();
    }
    return person;
}
```
Here we just take an element from the front of the queue and if it is null, we just make a new Person object
from the factory.

```java
public void returnObject(Person obj) {
    if (obj != null) {
        obj.reset();
        if (pool.size() < maxPoolSize) {
            pool.offer(obj);
        }
    }
}
```

Here for the reset I made a interface for the object reset:

```java
interface PoolObject {
    void reset();
}
```

Then I implemented the reset:

```java
@Override
public void reset() {
    this.firstName = null;
    this.lastName = null;
    this.age = 0;
    this.address = null;
    this.phone = null;
}
```

Now I can borrow and return objects when I need it:

```java
Person person1 = resourcePool.borrowObject();
person1.setFirstName("Resource 1");
person1.setLastName("Damn");
System.out.println("Borrowed: " + person1);

Person person2 = resourcePool.borrowObject();
person2.setFirstName("Resource 1");
person2.setLastName("Damn");
System.out.println("Borrowed: " + person2);

resourcePool.returnObject(person1);
resourcePool.returnObject(person2);

Person person3 = resourcePool.borrowObject();
System.out.println("Reused: " + person3);

resourcePool.returnObject(person3);
```

### Factories:
I also implemented factories for fun, but I need only for the report so, I wont write about them.

## Conclusion

In conclusion, I have made a singleton PersonObjectPool which can lend and retrieve Person objects, which can be created using a Builder, and can be dublicated using the Prototype pattern.