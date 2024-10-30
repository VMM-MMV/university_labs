package crazy.demo.files;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import crazy.demo.exception.FileProcessingException;
import crazy.demo.exception.FileValidationException;
import crazy.demo.game.Game;
import crazy.demo.game.GameRepository;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import java.io.IOException;
import java.util.List;

@Service
public class FileUploadService {

    private final GameRepository gameRepository;

    private final ObjectMapper objectMapper;

    public FileUploadService(GameRepository gameRepository, ObjectMapper objectMapper) {
        this.gameRepository = gameRepository;
        this.objectMapper = objectMapper;
    }

    public FileUploadResponse uploadGamesFile(MultipartFile file) {
        validateFile(file);

        try {
            List<Game> games = parseJsonFile(file);
            List<Game> savedGames = gameRepository.saveAll(games);

            return FileUploadResponse.builder()
                    .filename(file.getOriginalFilename())
                    .size(file.getSize())
                    .contentType(file.getContentType())
                    .recordsProcessed(savedGames.size())
                    .success(true)
                    .message("File processed successfully")
                    .build();

        } catch (IOException e) {
            throw new FileProcessingException("Error processing file: " + e.getMessage());
        }
    }

    private void validateFile(MultipartFile file) {
        if (file.isEmpty()) {
            throw new FileValidationException("File is empty");
        }

        String contentType = file.getContentType();
        if (contentType == null || !contentType.equals("application/json")) {
            throw new FileValidationException("Only JSON files are supported");
        }
    }

    private List<Game> parseJsonFile(MultipartFile file) throws IOException {
        try {
            return objectMapper.readValue(
                    file.getInputStream(),
                    new TypeReference<>() {}
            );
        } catch (IOException e) {
            throw new FileProcessingException("Error parsing JSON file: " + e.getMessage());
        }
    }
}