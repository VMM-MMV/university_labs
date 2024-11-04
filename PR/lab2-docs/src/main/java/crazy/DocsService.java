package crazy;

import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import org.springframework.context.annotation.Bean;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;
import org.springframework.stereotype.Service;

import java.util.ArrayDeque;
import java.util.concurrent.locks.ReentrantLock;

@Service
public class DocsService {
    private final ReentrantLock lock = new ReentrantLock();
    private final PriorityRequestQueue deque = new PriorityRequestQueue();
    private final ContentManager contentManager = ContentManager.getInstance();
    private final TaskExecutor taskExecutor;
    private volatile boolean running = true;
    private Thread queueMonitorThread;

    public DocsService() {
        this.taskExecutor = createTaskExecutor();
    }

    @Bean
    private static TaskExecutor createTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(10);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("docs-handler-");
        executor.initialize();
        return executor;
    }

    @PostConstruct
    public void startQueueMonitor() {
        queueMonitorThread = new Thread(this::monitorQueue, "docs-queue-monitor");
        queueMonitorThread.start();
    }

    @PreDestroy
    public void shutdown() {
        running = false;
        if (queueMonitorThread != null) {
            queueMonitorThread.interrupt();
        }
        if (taskExecutor instanceof ThreadPoolTaskExecutor) {
            ((ThreadPoolTaskExecutor) taskExecutor).shutdown();
        }
    }

    private void monitorQueue() {
        while (running) {
            try {
                lock.lock();
                Request request = deque.peek();
                if (request != null && request.hasFinishedWaiting()) {
                    request = deque.poll();
                    Request finalRequest = request;
                    taskExecutor.execute(() -> processRequest(finalRequest));
                }
            } finally {
                lock.unlock();
            }

            // Small sleep to prevent busy-waiting
            try {
                Thread.sleep(10);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private void processRequest(Request request) {
        try {
            lock.lock();
            if ("WRITE".equals(request.getType())) {
                contentManager.setContent(request.getContent());
            } else if ("READ".equals(request.getType())) {
                System.out.println(contentManager.getContent());
            } else {
                throw new IllegalStateException("Only READ and WRITE are allowed");
            }
        } finally {
            lock.unlock();
        }
    }

    public void addToQueue(Request request) {
        try {
            lock.lock();
            deque.offer(request);
        } finally {
            lock.unlock();
        }
    }
}