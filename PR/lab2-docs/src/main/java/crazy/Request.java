package crazy;

import lombok.Getter;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.Random;

@Getter
public class Request {
    private final String content;
    private final String type;
    private final LocalDateTime end;

    public Request(String content, String type) {
        this.content = content;
        this.type = type;
        this.end = LocalDateTime.now().plusSeconds(new Random().nextInt(7) + 1);
    }

    public boolean hasFinishedWaiting() {
        return Duration.between(end, LocalDateTime.now()).getSeconds() <= 0;
    }
}
