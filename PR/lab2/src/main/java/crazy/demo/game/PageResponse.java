package crazy.demo.game;

import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
public class PageResponse<T> {
    private List<T> content;
    private long totalElements;
    private int offset;
    private int limit;
    private int totalPages;

    @Builder.Default
    private boolean isFirst = false;

    @Builder.Default
    private boolean isLast = false;
}