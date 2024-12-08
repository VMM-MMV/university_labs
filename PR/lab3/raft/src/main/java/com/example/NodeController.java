package com.example;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.time.ZoneOffset;

@Slf4j
@RestController
@RequiredArgsConstructor
public class NodeController {

    private final NodeService nodeService;

    @PostMapping("/leader/health")
    public ResponseEntity<String> leaderHealthCheck(@RequestBody String payload) {
        try {
            nodeService.setLastLeaderAliveTime(LocalDateTime.now().toInstant(ZoneOffset.UTC));
            return ResponseEntity.ok("Leader alive time updated");
        } catch (Exception e) {
            log.error("Leader health check failed", e);
            return ResponseEntity.internalServerError().body("Health check failed");
        }
    }

    @PostMapping("/vote")
    public ResponseEntity<NodeService.VoteResponse> vote(@RequestBody NodeService.VoteRequest voteRequest) {
        try {
            NodeService.VoteResponse response = nodeService.handleVoteRequest(voteRequest);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            log.error("Vote request processing failed", e);
            return ResponseEntity.internalServerError().build();
        }
    }
}