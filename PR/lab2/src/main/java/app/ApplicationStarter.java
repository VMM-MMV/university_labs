package app;

import app.chat.ChatApplication;
import app.crud.GameApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.core.task.TaskExecutor;
import org.springframework.scheduling.concurrent.ThreadPoolTaskExecutor;

@SpringBootApplication
public class ApplicationStarter {

    public static void main(String[] args) {
        TaskExecutor taskExecutor = createTaskExecutor();

        String gamePort = System.getenv().getOrDefault("GAME_SERVER_PORT", "8080");
        String chatPort = System.getenv().getOrDefault("CHAT_SERVER_PORT", "8081");

        System.out.println(gamePort + " " + chatPort);

        taskExecutor.execute(() -> {
            SpringApplicationBuilder gameApp = new SpringApplicationBuilder(GameApplication.class)
                    .properties(
                            "server.port=" + gamePort,
                            "server.contextPath=/GameService",
                            "spring.jmx.default-domain=game",
                            "spring.application.admin.jmx-name=org.springframework.boot:type=Admin,name=GameApplication"
                    );
            gameApp.run(args);
            System.out.println("Game Application started on port " + gamePort);
        });

        taskExecutor.execute(() -> {
            SpringApplicationBuilder chatApp = new SpringApplicationBuilder(ChatApplication.class)
                    .properties(
                            "server.port=" + chatPort,
                            "server.contextPath=/ChatService",
                            "spring.jmx.default-domain=chat",
                            "spring.application.admin.jmx-name=org.springframework.boot:type=Admin,name=ChatApplication"
                    );
            chatApp.run(args);
            System.out.println("Chat Application started on port " + chatPort);
        });
    }

    private static TaskExecutor createTaskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(2);
        executor.setMaxPoolSize(2);
        executor.setThreadNamePrefix("app-starter-");
        executor.initialize();
        return executor;
    }
}