package crazy;

import crazy.utils.ContentType;
import crazy.utils.HttpSender;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.stereotype.Component;

@Component
public class RabbitMQConsumer {

    public final RaftService raftService;
    private final HttpSender httpSender;

    public RabbitMQConsumer(RaftService raftService, HttpSender httpSender) {
        this.raftService = raftService;
        this.httpSender = httpSender;
    }

    @RabbitListener(queues = "queue")
    public void receiveMessage(String message) {
        System.out.println("Received: " + message);
        if (raftService.getLeaderUrl() == null || raftService.getLeaderUrl().isEmpty()) return;
        message = message.replace("'", "\"");
        message = message.replace("None", "null");
        httpSender.post(raftService.getLeaderUrl() + "/iepure", message, ContentType.APPLICATION_JSON);
    }
}
