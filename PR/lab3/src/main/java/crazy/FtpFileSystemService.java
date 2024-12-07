package crazy;

import lombok.extern.slf4j.Slf4j;
import org.springframework.integration.file.remote.session.SessionFactory;
import org.springframework.integration.ftp.session.FtpRemoteFileTemplate;
import org.springframework.stereotype.Service;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.InputStream;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

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

    public InputStream readFile(String path) throws Exception {
        try (var session = ftpSessionFactory.getSession()) {
            return new BufferedInputStream(session.readRaw(path));
        }
    }

    public void deleteFile(String path) throws Exception {
        try (var session = ftpSessionFactory.getSession()) {
            session.remove(path);
        }
    }
}
