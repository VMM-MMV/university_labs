package src.notfactories;

import src.notfactories.interfaces.ObjectFactory;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.locks.ReentrantLock;

class PersonObjectPool {
    private final BlockingQueue<Person> pool;
    private final int maxPoolSize;
    private final ObjectFactory<Person> objectFactory;
    private static final ReentrantLock lock = new ReentrantLock();

    private static volatile PersonObjectPool instance;

    private PersonObjectPool(int maxPoolSize, ObjectFactory<Person> objectFactory) {
        this.maxPoolSize = maxPoolSize;
        this.objectFactory = objectFactory;
        this.pool = new LinkedBlockingQueue<>(maxPoolSize);
    }

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

    public Person borrowObject() {
        Person person = pool.poll();
        if (person == null) { person = objectFactory.createObject(); }
        return person;
    }

    public void returnObject(Person obj) {
        if (obj == null) { return; }

        obj.reset();
        if (pool.size() < maxPoolSize) {
            pool.offer(obj);
        }
    }
}