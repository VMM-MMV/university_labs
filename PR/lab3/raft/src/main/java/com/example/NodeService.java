package com.example;

import com.example.config.AppInfo;
import com.example.utils.ContentType;
import com.example.utils.HttpSender;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Random;

@Component
@Getter
@Setter
public class NodeService {

    public record VoteBallot(int term, int logIndex) { }

    private final HttpSender httpSender;
    private final Random random = new Random();
    private final AppInfo appInfo;

    @Value("${node.timeout.max}")
    private int maxTimeout;

    @Value("${node.timeout.min}")
    private int minTimeout;

    @Value("${manager.url}")
    private String managerUrl;

    private List<String> nodes = new ArrayList<>();

    private boolean isLeader = false;
    private LocalDateTime lastLeaderAliveTime = LocalDateTime.now();
    private int term;
    private ArrayList<String> log;
    private String uncommitedLogEntry;

    public NodeService(HttpSender httpSender, AppInfo appInfo) {
        this.httpSender = httpSender;
        this.appInfo = appInfo;
    }

    public void doLeaderJob() {
        if (!isLeader) return;

        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl + "/leader/health", "I am ALIVE!", ContentType.APPLICATION_JSON));
    }

    public void leaderSendLog(String message) {
        long appendedNodes = nodes.parallelStream()
                .map(nodeUrl -> {
                    ResponseEntity<String> response = httpSender.post(nodeUrl + "/nodes/log/append", "{logIndex: " + this.log.size() + ", message: " + message + "}", ContentType.APPLICATION_JSON);

                    if (Objects.equals("Outdated Log", response.getBody())) { httpSender.post(nodeUrl + "/nodes/log/sync", log.toString(), ContentType.APPLICATION_JSON); }
                    return response;
                })
                .filter(response -> response.getStatusCode().is2xxSuccessful())
                .count();

        if (appendedNodes < nodes.size() / 2) {
            nodes.parallelStream().forEach(nodeUrl -> httpSender.post(nodeUrl + "/nodes/log/append", "", ContentType.APPLICATION_JSON));
            throw new RuntimeException(nodes.size() - appendedNodes + " nodes did not finish appending their log.");
        }

        log.add(message);
        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl + "/nodes/log/commit", "Commit your stuff bruh", ContentType.APPLICATION_JSON));
    }

    public void doNodeJob() throws InterruptedException {
        int randomWaitPeriod = random.nextInt(maxTimeout - minTimeout + 1);
        Thread.sleep(randomWaitPeriod);
        boolean leaderHealthCheckIsTooOld = LocalDateTime.now().minusNanos(randomWaitPeriod + minTimeout).isAfter(lastLeaderAliveTime);
        if (leaderHealthCheckIsTooOld) requestVotes();
    }

    public void updateNodes(List<String> nodes) {
        nodes.remove(appInfo.getUrl());
        this.nodes = nodes;
    }

    public void joinNodes() {
        httpSender.post(managerUrl + "/node", appInfo.getUrl(), ContentType.APPLICATION_JSON);
    }

    public ResponseEntity<String> syncLog(ArrayList<String> incomingLog) {
        if (incomingLog == null || incomingLog.isEmpty()) {
            return ResponseEntity.badRequest().body("Invalid log received");
        }

        if (incomingLog.size() > log.size()) {
            log.clear();
            log.addAll(incomingLog);
            uncommitedLogEntry = null;
            return ResponseEntity.ok("Log synchronized successfully");
        } else {
            return ResponseEntity.status(409).body("Local log is up-to-date or more recent");
        }
    }

    public ResponseEntity<String> appendLog(int logIndex, String message) {
        if (logIndex > log.size()) return ResponseEntity.ok("Outdated Log");
        uncommitedLogEntry = message;
        return ResponseEntity.ok("Appended successfully");
    }

    public void commitLog() {
        if (uncommitedLogEntry == null || uncommitedLogEntry.isEmpty()) { throw new RuntimeException("There is no appended log entry"); }
        log.add(uncommitedLogEntry);
        uncommitedLogEntry = null;
    }

    public boolean voteForCandidate(VoteBallot voteBallot) {
        if (voteBallot.term <= this.term) { return false; }
        if (voteBallot.logIndex < this.log.size()) { return false; }
        this.term++;
        return true;
    }

    private void requestVotes() {
        long votes = nodes.parallelStream()
                .map(nodeUrl -> httpSender.post(nodeUrl + "/vote", makeVoteJson(), ContentType.APPLICATION_JSON))
                .filter(x -> Boolean.parseBoolean(x.getBody()))
                .count();

        if (votes >= nodes.size() / 2) { isLeader = true; }
    }

    private String makeVoteJson() {
        return "{" +
                "   term: " + term +
                "   logIndex: " + this.log.size() +
                "}";
    }
}
