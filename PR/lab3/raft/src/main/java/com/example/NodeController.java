package com.example;

import com.example.model.Game;
import com.example.model.Summary;
import com.example.repository.GameRepository;
import com.example.repository.SummaryRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.time.ZoneOffset;
import java.util.List;

@Slf4j
@RestController
@RequiredArgsConstructor
public class NodeController {

    private final NodeService nodeService;

    private GameRepository gameRepository;

    private SummaryRepository summaryRepository;

    @Autowired
    public NodeController(NodeService nodeService, GameRepository gameRepository, SummaryRepository summaryRepository) {
        this.nodeService = nodeService;
        this.gameRepository = gameRepository;
        this.summaryRepository = summaryRepository;
    }

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

    @PostMapping("/ftp")
    public ResponseEntity<String> receiveFTPMessage(@RequestBody Summary summary) {
        summaryRepository.save(summary);
        return ResponseEntity.ok("Summary received");
    }

    @GetMapping("/ftp")
    public List<Summary> getAllFtpMessages() {
        return summaryRepository.findAll();
    }

    @PostMapping("/iepure")
    public ResponseEntity<String> receiveIepureMessage(@RequestBody List<Game> games) {
        gameRepository.saveAll(games);
        return ResponseEntity.ok("Games received");
    }

    @GetMapping("/iepure")
    public List<Game> getAllIepureMessages() {
        return gameRepository.findAll();
    }
}