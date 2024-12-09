package crazy;

import crazy.utils.ContentType;
import crazy.utils.HttpSender;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.List;

@Component
public class FtpSchedule {

    private final HttpSender httpSender;
    private final RaftService raftService;

    private final FtpFileSystemService ftpFileSystemService;

    public FtpSchedule(FtpFileSystemService ftpFileSystemService, HttpSender httpSender, RaftService raftService) {
        this.ftpFileSystemService = ftpFileSystemService;
        this.httpSender = httpSender;
        this.raftService = raftService;
    }

    private boolean first = true;

    @Scheduled(fixedRate = 30 * 1000)
    public void readFtp() {
        if (first) {first = false; return;}
        List<File> res = ftpFileSystemService.listFiles("/");
        if (raftService.getLeaderUrl() == null || raftService.getLeaderUrl().isEmpty()) return;
        res.parallelStream()
                .peek(System.out::println)
                .map(x -> ftpFileSystemService.readFile(x.getPath()))
                .forEach(fileContent -> httpSender.post(raftService.getLeaderUrl() + "/ftp", fileContent, ContentType.APPLICATION_JSON));

        res.parallelStream()
                .forEach(file -> ftpFileSystemService.deleteFile(file.getPath()));
    }
}