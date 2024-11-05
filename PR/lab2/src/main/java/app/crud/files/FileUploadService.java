package app.crud.files;

import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

@Service
public class FileUploadService {

    public Map<String, Object> processFileUpload(MultipartFile file, String description) throws IOException {
        // Print file details
        System.out.println("File Name: " + file.getOriginalFilename());
        System.out.println("File Size: " + file.getSize() + " bytes");
        System.out.println("Content Type: " + file.getContentType());
        System.out.println("Description: " + description);

        // Process file content
        byte[] content = file.getBytes();
        System.out.println("File Content Length: " + content.length);

        // Create response
        Map<String, Object> response = new HashMap<>();
        response.put("message", "File uploaded successfully");
        response.put("fileName", file.getOriginalFilename());
        response.put("fileSize", file.getSize());
        response.put("contentType", file.getContentType());
        response.put("description", description);

        return response;
    }
}
