package com.example;

import com.example.config.AppInfo;
import com.example.utils.ContentType;
import com.example.utils.HttpSender;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import lombok.Getter;
import lombok.Setter;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;

import java.time.Duration;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicBoolean;
import java.util.concurrent.atomic.AtomicInteger;

@Component
@Getter
@Setter
@Slf4j
public class NodeService {
    public record VoteRequest(int term, int logIndex, String candidateId) {}
    public record VoteResponse(boolean voteGranted, int term) {}

    private final HttpSender httpSender;
    private final Random random = new Random();
    private final AppInfo appInfo;
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final ExecutorService voteExecutor = Executors.newFixedThreadPool(10);

    @Value("${node.timeout.max}")
    private int maxTimeout;

    @Value("${node.timeout.min}")
    private int minTimeout;

    @Value("${manager.url}")
    private String managerUrl;

    private final AtomicBoolean isLeader = new AtomicBoolean(false);
    private volatile Instant lastLeaderAliveTime = Instant.now();

    private final AtomicInteger currentTerm = new AtomicInteger(0);

    private final List<String> raftLog = new ArrayList<>();
    private volatile String uncommittedLogEntry;

    @Autowired
    public NodeService(HttpSender httpSender, AppInfo appInfo) {
        this.httpSender = httpSender;
        this.appInfo = appInfo;
    }

    public void leaderHeartbeat() {
        if (!isLeader.get()) return;

        Set<String> nodes = getNodes();

        try {
            nodes.parallelStream()
                    .forEach(nodeUrl -> {
                        try {
                            httpSender.post(nodeUrl + "/leader/health", createHeartbeatPayload(), ContentType.APPLICATION_JSON);
                        } catch (Exception e) {
                            log.warn("Heartbeat to {} failed", nodeUrl);
                        }
                    });
        } catch (Exception e) {
            log.error("Heartbeat process failed", e);
        }
    }

    private Set<String> getNodes() {
        Set<String> nodes =  httpSender.getNodes(managerUrl + "/nodes");
        System.out.println("nodes " + nodes);
        nodes.remove(appInfo.getUrl());
        return nodes;
    }

    public void nodeElectionTimeout() {
        System.out.println(appInfo.getUrl() + " " + isLeader.get());
        if (isLeader.get()) return;

        int randomWaitPeriod = random.nextInt(maxTimeout - minTimeout + 1) + minTimeout;

        try {
            Thread.sleep(randomWaitPeriod);

            boolean isLeaderTimedOut = Instant.now()
                        .isAfter(lastLeaderAliveTime.plus(Duration.ofMillis(minTimeout + randomWaitPeriod)));

            if (isLeaderTimedOut) { startElection(); }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            log.error("Election timeout interrupted", e);
        }
    }

    private void startElection() {
        int electionTerm = currentTerm.incrementAndGet();

        VoteRequest voteRequest = new VoteRequest(
                electionTerm,
                raftLog.size(),
                appInfo.getUrl()
        );

        Set<String> nodes = getNodes();

        System.out.println(appInfo.getUrl() + " " + nodes);

        try {
            long successfulVotes = nodes.parallelStream()
                    .map(nodeUrl -> requestVoteFromNode(nodeUrl, voteRequest))
                    .filter(Boolean::valueOf)
                    .count();

            if (successfulVotes > nodes.size() / 2 || nodes.isEmpty()) {
                becomeLeader();
            }
        } catch (Exception e) {
            log.error("Election process failed", e);
        }
    }

    private boolean requestVoteFromNode(String nodeUrl, VoteRequest voteRequest) {
        try {
            ResponseEntity<String> response = httpSender.post(nodeUrl + "/vote", objectMapper.writeValueAsString(voteRequest), ContentType.APPLICATION_JSON);

            VoteResponse voteResponse = objectMapper.readValue(
                    response.getBody(), VoteResponse.class
            );

            return voteResponse.voteGranted();
        } catch (Exception e) {
            log.warn("Vote request to {} failed", nodeUrl, e);
            return false;
        }
    }

    public VoteResponse handleVoteRequest(VoteRequest request) {
        synchronized (this) {
            if (request.term() < currentTerm.get()) {
                return new VoteResponse(false, currentTerm.get());
            }

            if (request.term() > currentTerm.get()) {
                currentTerm.set(request.term());
                isLeader.set(false);
            }

            boolean logOK = request.logIndex() >= raftLog.size();

            return new VoteResponse(logOK, currentTerm.get());
        }
    }

    private void becomeLeader() {
        isLeader.set(true);
        updateManagerLeader();
        leaderHeartbeat();
    }

    private void updateManagerLeader() {
        httpSender.post(managerUrl + "/leader", appInfo.getUrl(), ContentType.APPLICATION_JSON);
    }

    private String createHeartbeatPayload() {
        try {
            return objectMapper.writeValueAsString(
                    new VoteRequest(currentTerm.get(), raftLog.size(), appInfo.getUrl())
            );
        } catch (JsonProcessingException e) {
            log.error("Failed to create heartbeat payload", e);
            return "{}";
        }
    }

    public void joinNodes() {
        httpSender.post(managerUrl + "/nodes", appInfo.getUrl(), ContentType.APPLICATION_JSON);
    }
}