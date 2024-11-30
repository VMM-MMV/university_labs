package com.example;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

@Component
public class JobScheduler {

    private final NodeService nodeService;

    public JobScheduler(NodeService nodeService) {
        this.nodeService = nodeService;
    }

    @Scheduled(fixedRateString = "${leader.heartbeat}")
    private void leaderJob() {
        nodeService.doLeaderJob();
    }

    @Scheduled(fixedRateString = "${node.timeout.min}")
    public void nodeJob() throws InterruptedException {
        nodeService.doNodeJob();
    }
}
