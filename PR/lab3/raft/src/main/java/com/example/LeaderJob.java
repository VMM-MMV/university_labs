package com.example;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class LeaderJob {

    private final NodeService nodeService;

    public LeaderJob(NodeService nodeService) {
        this.nodeService = nodeService;
    }

    @Scheduled(fixedRateString = "${leader.heartbeat}")
    private void leaderJob() {
        nodeService.doLeaderJob();
    }
}
