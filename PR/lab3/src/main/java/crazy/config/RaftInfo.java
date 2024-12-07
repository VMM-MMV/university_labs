package crazy.config;

import lombok.Data;
import org.springframework.stereotype.Component;

import java.util.Set;

@Component
@Data
public class RaftInfo {
    private String leaderUrl;
    private Set<String> nodes;
}
