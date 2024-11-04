package crazy;

import java.util.Comparator;
import java.util.PriorityQueue;
import java.util.concurrent.locks.ReentrantLock;

public class PriorityRequestQueue {
    private final PriorityQueue<Request> queue;
    private final ReentrantLock lock = new ReentrantLock();

    public PriorityRequestQueue() {
        Comparator<Request> requestComparator = (r1, r2) -> {
            if (r1.getType().equals("WRITE") && !r2.getType().equals("WRITE")) { return -1; }
            if (!r1.getType().equals("WRITE") && r2.getType().equals("WRITE")) { return 1; }
            // If types are the same, compare by endTime
            return r1.getEnd().compareTo(r2.getEnd());
        };
        this.queue = new PriorityQueue<>(requestComparator);
    }

    public void offer(Request request) {
        try {
            lock.lock();
            queue.offer(request);
        } finally {
            lock.unlock();
        }
    }

    public Request poll() {
        try {
            lock.lock();
            return queue.poll();
        } finally {
            lock.unlock();
        }
    }

    public Request peek() {
        try {
            lock.lock();
            return queue.peek();
        } finally {
            lock.unlock();
        }
    }
}