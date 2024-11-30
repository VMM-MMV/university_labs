package crazy.ftp;

import crazy.util.StreamConvertor;

import crazy.web.Sender;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.io.File;
import java.io.InputStream;
import java.util.List;

@Component
public class FtpSchedule {

    private final FtpFileSystemService ftpFileSystemService;
    private final Sender sender;

    public FtpSchedule(FtpFileSystemService ftpFileSystemService, Sender sender) {
        this.ftpFileSystemService = ftpFileSystemService;
        this.sender = sender;
    }

    @Scheduled(fixedRate = 5 * 1000)
    public void readFtp() {
        List<File> res = ftpFileSystemService.listFiles("/");
        res.stream()
                .peek(System.out::println)
                .forEach(x -> {
                    try {
                        InputStream fileContent = ftpFileSystemService.readFile(x.getPath());
                        String stringFileContent = StreamConvertor.convertInputStreamToString(fileContent);
                        sender.post(stringFileContent);
                    } catch (Exception e) {
                        throw new RuntimeException(e);
                    }
                });
    }
}