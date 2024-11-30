package com.example;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
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

    @PostMapping("/nodes/log/append")
    public ResponseEntity<String> appendLog(@RequestBody String message) {
        nodeService.appendLog(message);
        return ResponseEntity.ok("Updated log");
    }

    @PostMapping("/nodes/log/commit")
    public ResponseEntity<String> commitLog(@RequestBody String message) {
        nodeService.commitLog();
        return ResponseEntity.ok("Updated log");
    }
}
