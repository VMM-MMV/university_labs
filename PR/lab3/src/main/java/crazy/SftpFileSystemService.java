package crazy;

import lombok.extern.slf4j.Slf4j;
import org.apache.sshd.sftp.client.SftpClient;
import org.springframework.integration.file.remote.session.SessionFactory;
import org.springframework.integration.sftp.session.SftpRemoteFileTemplate;
import org.springframework.stereotype.Service;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.util.Arrays;
import java.util.List;

@Slf4j
@Service
public class SftpFileSystemService {

    private final SessionFactory<SftpClient.DirEntry> sftpSessionFactory;
    private final SftpRemoteFileTemplate sftpRemoteFileTemplate;

    public SftpFileSystemService(SessionFactory<SftpClient.DirEntry> sftpSessionFactory, SftpRemoteFileTemplate sftpRemoteFileTemplate) {
        this.sftpSessionFactory = sftpSessionFactory;
        this.sftpRemoteFileTemplate = sftpRemoteFileTemplate;
    }

    public List<File> listFiles(String path) {
        return sftpRemoteFileTemplate.execute(session ->
                Arrays.stream(session.list(path))
                        .map(x -> new File(path, x.getFilename()))
                        .toList()
        );
    }

    public InputStream readFile(String path) throws IOException {
        return new BufferedInputStream(sftpSessionFactory.getSession().readRaw(path));
    }

    public void deleteFile(String path) throws IOException {
        sftpSessionFactory.getSession().remove(path);
    }
}
