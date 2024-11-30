package com.example;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

import java.time.LocalDateTime;
import java.util.Random;

@RestController
public class NodeController {

    private LocalDateTime lastLeaderAliveTime;
    private final Random random = new Random();

    @Value("${node.timeout.max}")
    private int minTimeout;

    @Value("${node.timeout.min}")
    private int maxTimeout;

    @PostMapping("/leader/health")
    public ResponseEntity<String> leaderHealthCheck() {
        lastLeaderAliveTime = LocalDateTime.now();
        return ResponseEntity.ok("Leader alive time updated");
    }

    @Scheduled(fixedRateString = "${node.timeout.min}")
    public void nodeJob() throws InterruptedException {
        Thread.sleep(random.nextInt(maxTimeout - minTimeout + 1));

    }
}
