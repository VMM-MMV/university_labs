package com.example;

import com.example.utils.ContentType;
import com.example.utils.HttpSender;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Component
@Getter
@Setter
public class NodeService {

    public record VoteBallot(int term, int logIndex) { }

    private final HttpSender httpSender;
    private final Random random = new Random();

    @Value("${node.timeout.max}")
    private int minTimeout;

    @Value("${node.timeout.min}")
    private int maxTimeout;

    private List<String> nodes = new ArrayList<>();

    private boolean isLeader = false;
    private LocalDateTime lastLeaderAliveTime;
    private int term;
    private ArrayList<String> log;
    private String uncommitedLogEntry;

    public NodeService(HttpSender httpSender) {
        this.httpSender = httpSender;
    }

    public void doLeaderJob() {
        if (!isLeader) return;

        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl + "/leader/health", "I am ALIVE!", ContentType.APPLICATION_JSON));
    }

    @Transactional
    public void leaderSendLog(String message) {
        log.add(message);

        long appendedNodes = nodes.parallelStream()
                                    .map(nodeUrl -> httpSender.post(nodeUrl + "/nodes/log/append", message, ContentType.APPLICATION_JSON))
                                    .filter(response -> response != null && response.getStatusCode().is2xxSuccessful())
                                    .count();

        if (appendedNodes < nodes.size() / 2) {
            nodes.parallelStream().forEach(nodeUrl -> httpSender.post(nodeUrl + "/nodes/log/append", "", ContentType.APPLICATION_JSON));
            throw new RuntimeException(nodes.size() - appendedNodes + " nodes did not finish appending their log.");
        }

        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl + "/nodes/log/commit", "Commit your stuff bruh", ContentType.APPLICATION_JSON));
    }

    public void doNodeJob() throws InterruptedException {
        int randomWaitPeriod = random.nextInt(maxTimeout - minTimeout + 1);
        Thread.sleep(randomWaitPeriod);
        boolean leaderHealthCheckIsTooOld = LocalDateTime.now().minusNanos(randomWaitPeriod + minTimeout).isAfter(lastLeaderAliveTime);
        if (leaderHealthCheckIsTooOld) requestVotes();
    }

    public void appendLog(String message) {
        uncommitedLogEntry = message;
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
