package crazy;

import crazy.config.RaftInfo;
import crazy.utils.ContentType;
import crazy.utils.HttpSender;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController("manager/raft")
public class RaftController {

    private final RaftInfo raftInfo;
    private final HttpSender httpSender;

    public RaftController(RaftInfo raftInfo, HttpSender httpSender) {
        this.raftInfo = raftInfo;
        this.httpSender = httpSender;
    }

    @PostMapping("leader")
    public void updateLeader(@RequestBody String leaderUrl) {
        raftInfo.getNodes().remove(leaderUrl);
        raftInfo.setLeaderUrl(leaderUrl);
        System.out.println(raftInfo.getNodes() + " " + raftInfo.getLeaderUrl());
    }

    @PostMapping("node")
    public void addNode(@RequestBody String nodeUrl) {
        raftInfo.getNodes().add(nodeUrl);
        raftInfo.getNodes().stream().parallel()
                .filter(x -> !x.equals(nodeUrl))
                .forEach(x -> httpSender.post(x + "/nodes", raftInfo.getNodes().toString(), ContentType.APPLICATION_JSON));
        System.out.println(raftInfo.getNodes() + " " + raftInfo.getLeaderUrl());
    }
}
