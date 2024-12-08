package crazy;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.HashSet;
import java.util.Set;

@RestController("manager/raft")
public class RaftController {

    private String leaderUrl;
    private final Set<String> nodes = new HashSet<>();

    @PostMapping("leader")
    public void updateLeader(@RequestBody String leaderUrl) {
        nodes.remove(leaderUrl);
        this.leaderUrl = leaderUrl;
    }

    @PostMapping("nodes")
    public void addNode(@RequestBody String nodeUrl) {
        nodes.add(nodeUrl);
    }

    @GetMapping("nodes")
    public Set<String> getNodes() {
        return nodes;
    }
}
