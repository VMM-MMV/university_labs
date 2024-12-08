package com.example;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Bean;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Slf4j
@Component
@RequiredArgsConstructor
public class JobScheduler {

    private final NodeService nodeService;

    private boolean firstRound = true;

    @Scheduled(fixedRateString = "${leader.heartbeat}")
    public void leaderHeartbeatJob() {
        try {
            nodeService.leaderHeartbeat();
        } catch (Exception e) {
            log.error("Leader heartbeat job failed", e);
        }
    }

    @Scheduled(fixedRateString = "${node.timeout.min}")
    public void nodeElectionTimeoutJob() {
        if (firstRound) { firstRound = false; return; }
        try {
            nodeService.nodeElectionTimeout();
        } catch (Exception e) {
            log.error("Node election timeout job failed", e);
        }
    }

    @Bean
    public int notifyManager() {
        nodeService.joinNodes();
        return 0;
    }
}