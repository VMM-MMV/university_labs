package com.example;

import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;

@RestController
public class NodeController {

    private LocalDateTime lastLeaderAliveTime;

    @PostMapping("/leader/health")
    public ResponseEntity<String> leaderHealthCheck() {
        lastLeaderAliveTime = LocalDateTime.now();
        return ResponseEntity.ok("Leader alive time updated");
    }

    @Scheduled(fixedRateString = "${node.timeout}")
    public void nodeJob() {

    }
}
