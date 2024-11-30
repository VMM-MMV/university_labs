package com.example;

import com.example.utils.ContentType;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;
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
}
