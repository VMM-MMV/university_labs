package crazy;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.Set;

@RestController("manager/raft")
public class RaftController {

    private final RaftService raftService;

    public RaftController(RaftService raftService) {
        this.raftService = raftService;
    }

    @PostMapping("leader")
    public void updateLeader(@RequestBody String leaderUrl) {
        System.out.println("manager" + " " + leaderUrl);
        raftService.updateLeader(leaderUrl);
    }

    @PostMapping("nodes")
    public void addNode(@RequestBody String nodeUrl) {
        raftService.addNode(nodeUrl);
    }

    @GetMapping("nodes")
    public Set<String> getNodes() {
        return raftService.getNodes();
    }
}
