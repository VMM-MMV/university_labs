package docs;

import java.util.concurrent.locks.ReentrantLock;

public class ContentManager {
    private static ContentManager instance;
    private static StringBuilder content;

    private static ReentrantLock lock;

    public static ContentManager getInstance() {
        if (instance == null) {
            try {
                lock.lock();
                if (instance == null) {
                    instance = new ContentManager();
                }
            } finally {
                lock.unlock();
            }
        }
        return instance;
    }

    public String getContent() {
        return content.toString();
    }

    public void setContent(String newContent) {
        try {
            lock.lock();
            content.append(newContent);
        } finally {
            lock.unlock();
        }
    }
}
