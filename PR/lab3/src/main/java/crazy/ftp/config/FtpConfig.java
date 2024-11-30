package crazy.ftp.config;

import lombok.Getter;
import lombok.Setter;
import org.apache.commons.net.ftp.FTPFile;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.file.remote.session.SessionFactory;
import org.springframework.integration.ftp.session.DefaultFtpSessionFactory;
import org.springframework.integration.ftp.session.FtpRemoteFileTemplate;

@Configuration
@ConfigurationProperties(prefix = "sftp")
@Getter
@Setter
public class FtpConfig {

    private String host;
    private int port;
    private String user;
    private String password;

    @Bean
    public SessionFactory<?> ftpSessionFactory() {
        DefaultFtpSessionFactory factory = new DefaultFtpSessionFactory();
        factory.setHost(host);
        factory.setPort(port);
        factory.setUsername(user);
        factory.setPassword(password);
        factory.setClientMode(2);
        return factory;
    }

    @Bean
    public FtpRemoteFileTemplate ftpRemoteFileTemplate(SessionFactory<FTPFile> ftpSessionFactory) {
        return new FtpRemoteFileTemplate(ftpSessionFactory);
    }
}