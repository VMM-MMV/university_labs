package crazy;

import lombok.extern.slf4j.Slf4j;
import org.springframework.integration.file.remote.session.SessionFactory;
import org.springframework.integration.ftp.session.FtpRemoteFileTemplate;
import org.springframework.stereotype.Service;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
public class FtpFileSystemService {

    private final SessionFactory<?> ftpSessionFactory;
    private final FtpRemoteFileTemplate ftpRemoteFileTemplate;

    public FtpFileSystemService(SessionFactory<?> ftpSessionFactory, FtpRemoteFileTemplate ftpRemoteFileTemplate) {
        this.ftpSessionFactory = ftpSessionFactory;
        this.ftpRemoteFileTemplate = ftpRemoteFileTemplate;
    }

    public List<File> listFiles(String path) {
        try {
            return ftpRemoteFileTemplate.execute(session -> {
                try {
                    return Arrays.stream(session.list(path))
                            .map(x -> new File(path, x.getName()))
                            .toList();
                } catch (Exception e) {
                    log.error("Error listing files in path: {}", path, e);
                    throw new RuntimeException("Failed to list files", e);
                }
            });
        } catch (Exception e) {
            log.error("FTP connection or listing failed", e);
            return Collections.emptyList();
        }
    }

    public String readFile(String path) {
        try (var session = ftpSessionFactory.getSession();
             var inputStream = new BufferedInputStream(session.readRaw(path));
             var reader = new BufferedReader(new InputStreamReader(inputStream, StandardCharsets.UTF_8))) {
            return reader.lines().collect(Collectors.joining("\n"));
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void deleteFile(String path) {
        try (var session = ftpSessionFactory.getSession()) {
            session.remove(path);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }
}
