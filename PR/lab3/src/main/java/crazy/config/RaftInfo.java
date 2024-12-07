package crazy.config;

import lombok.Data;
import org.springframework.stereotype.Component;

import java.util.HashSet;
import java.util.Set;

@Component
@Data
public class RaftInfo {
    private String leaderUrl;
    private final Set<String> nodes = new HashSet<>();
}
