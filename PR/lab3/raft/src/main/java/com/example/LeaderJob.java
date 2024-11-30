package com.example;

import com.example.utils.HttpSender;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Component
public class LeaderJob {
    private boolean isLeader = false;

    private List<String> nodes = new ArrayList<>();

    private final HttpSender httpSender;

    public LeaderJob(HttpSender httpSender) {
        this.httpSender = httpSender;
    }

    @Scheduled(fixedRateString = "${leader.heartbeat}")
    private void leaderJob() {
        if (!isLeader) return;

        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl, "I am ALIVE!"));
    }


}
