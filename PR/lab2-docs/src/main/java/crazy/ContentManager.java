package crazy;

import java.util.concurrent.locks.ReentrantLock;

public class ContentManager {
    private static ContentManager instance;
    private static final StringBuilder content = new StringBuilder();

    private static final ReentrantLock lock = new ReentrantLock();;

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
        content.append(newContent);
    }
}
