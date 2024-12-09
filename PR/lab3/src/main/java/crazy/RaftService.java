package crazy;


import lombok.Getter;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.Set;


@Getter
@Component
public class RaftService {
    private String leaderUrl;
    private final Set<String> nodes = new HashSet<>();

    public void updateLeader(String leaderUrl) {
        nodes.remove(leaderUrl);
        this.leaderUrl = leaderUrl;
    }

    public void addNode(String nodeUrl) {
        nodes.add(nodeUrl);
    }
}
