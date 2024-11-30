package com.example;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class Runner {
    private boolean isLeader = false;

    private List<String> nodes = new ArrayList<>();

    private final Sender sender;

    public Runner(Sender sender) {
        this.sender = sender;
    }

    @Scheduled(fixedRateString = "${leader.heartbeat}")
    private void leaderJob() {
        if (!isLeader) return;

        nodes.parallelStream()
                .forEach(nodeUrl -> sender.post(nodeUrl, "I am ALIVE!"));
    }


}
