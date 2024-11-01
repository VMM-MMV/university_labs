package app;

import app.chat.ChatApplication;
import app.crud.GameApplication;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@SpringBootApplication
public class ApplicationStarter {

    public static void main(String[] args) {
        TaskExecutor taskExecutor = createTaskExecutor();

        taskExecutor.execute(() -> startGameApplication(args));
        taskExecutor.execute(() -> startChatApplication(args));
    }

    private static TaskExecutor createTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(2);
        executor.initialize();
        return executor;
    }

    private static void startGameApplication(String[] args) {
        try {
            ConfigurableApplicationContext gameContext = SpringApplication.run(GameApplication.class, args);
            System.out.println("Game Application started on thread: " + Thread.currentThread().getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private static void startChatApplication(String[] args) {
        try {
            ConfigurableApplicationContext chatContext = SpringApplication.run(ChatApplication.class, args);
            System.out.println("Chat Application started on thread: " + Thread.currentThread().getName());
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}