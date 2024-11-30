package crazy.ftp;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.List;

@Component
public class FtpSchedule {

    private final FtpFileSystemService ftpFileSystemService;

    public FtpSchedule(FtpFileSystemService ftpFileSystemService) {
        this.ftpFileSystemService = ftpFileSystemService;
    }

    @Scheduled(fixedRate = 5 * 1000)
    public void readFtp() {
        List<File> res = ftpFileSystemService.listFiles("/");
        res.stream()
                .peek(System.out::println)
                .forEach(x -> {
                    try {
                        System.out.println(ftpFileSystemService.readFile(x.getPath()));
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                });
    }
}