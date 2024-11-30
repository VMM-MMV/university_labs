package com.example;

import com.example.utils.ContentType;
import com.example.utils.HttpSender;
import lombok.Getter;
import lombok.Setter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

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

    public NodeService(HttpSender httpSender) {
        this.httpSender = httpSender;
    }

    public void doLeaderJob() {
        if (!isLeader) return;

        nodes.parallelStream()
                .forEach(nodeUrl -> httpSender.post(nodeUrl + "/leader/health", "I am ALIVE!", ContentType.APPLICATION_JSON));
    }

    public void doNodeJob() throws InterruptedException {
        int randomWaitPeriod = random.nextInt(maxTimeout - minTimeout + 1);
        Thread.sleep(randomWaitPeriod);
        boolean leaderHealthCheckIsTooOld = LocalDateTime.now().minusNanos(randomWaitPeriod + minTimeout).isAfter(lastLeaderAliveTime);
        if (leaderHealthCheckIsTooOld) requestVotes();
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
                .filter(x -> Boolean.parseBoolean(x))
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
