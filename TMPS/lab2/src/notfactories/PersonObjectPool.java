package src.notfactories;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.locks.ReentrantLock;

class PersonObjectPool<T extends PoolObject> {
    private final BlockingQueue<T> pool;
    private final int maxPoolSize;
    private final ObjectFactory<T> objectFactory;
    private static final ReentrantLock lock = new ReentrantLock();

    private static volatile PersonObjectPool<Person> instance;

    private PersonObjectPool(int maxPoolSize, ObjectFactory<T> objectFactory) {
        this.maxPoolSize = maxPoolSize;
        this.objectFactory = objectFactory;
        this.pool = new LinkedBlockingQueue<>(maxPoolSize);
    }

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

    public T borrowObject() {
        T obj = pool.poll();
        if (obj == null) {
            obj = objectFactory.createObject();
        }
        return obj;
    }

    public void returnObject(T obj) {
        if (obj != null) {
            obj.reset();
            if (pool.size() < maxPoolSize) {
                pool.offer(obj);
            }
        }
    }
}