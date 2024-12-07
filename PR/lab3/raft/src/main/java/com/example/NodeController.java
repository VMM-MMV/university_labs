package com.example;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/raft/api/v1")
public class NodeController {

    private final NodeService nodeService;

    public NodeController(NodeService nodeService) {
        this.nodeService = nodeService;
    }

    @PostMapping("/leader/health")
    public ResponseEntity<String> leaderHealthCheck() {
        nodeService.setLastLeaderAliveTime(LocalDateTime.now());
        return ResponseEntity.ok("Leader alive time updated");
    }

    @PostMapping("/nodes/vote")
    public boolean vote(@RequestBody NodeService.VoteBallot voteBallot) {
        return nodeService.voteForCandidate(voteBallot);
    }

    @PostMapping("/nodes")
    public ResponseEntity<String> updateNodeList(@RequestBody List<String> nodes) {
        nodeService.updateNodes(nodes);
        return ResponseEntity.ok("Updated nodes");
    }
}
