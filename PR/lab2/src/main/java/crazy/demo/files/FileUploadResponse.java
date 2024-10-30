package crazy.demo.files;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class FileUploadResponse {
    private String filename;
    private long size;
    private String contentType;
    private int recordsProcessed;
    private boolean success;
    private String message;
}