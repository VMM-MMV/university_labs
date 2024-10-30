package crazy.demo.game;

import jakarta.annotation.PostConstruct;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.stereotype.Service;

import java.util.Arrays;
import java.util.List;

@Service
public class GameService {

    private final GameRepository gameRepository;

    public GameService(GameRepository gameRepository) {
        this.gameRepository = gameRepository;
    }

    public Game getById(Long id) {
        return gameRepository.getById(id);
    }

    public Game getByName(String name) {
        return gameRepository.getGameByName(name);
    }

    public Page<Game> getAllGames(int offset, int limit) {
        int page = offset / limit;
        return gameRepository.findAll(PageRequest.of(page, limit));
    }

    public Game getGameById(Long id) {
        return gameRepository.findById(id)
                .orElseThrow(() -> new GameNotFoundException("Game not found with id: " + id));
    }

    public Game getGameByName(String name) {
        Game game = gameRepository.getGameByName(name);
        if (game == null) {
            throw new GameNotFoundException("Game not found with name: " + name);
        }
        return game;
    }

    public Game createGame(Game game) {
        return gameRepository.save(game);
    }

    public Game updateGame(Long id, Game gameDetails) {
        if (!gameRepository.existsById(id)) {
            throw new GameNotFoundException("Game not found with id: " + id);
        }
        gameDetails.setId(id);
        return gameRepository.save(gameDetails);
    }

    public void deleteGame(Long id) {
        if (!gameRepository.existsById(id)) {
            throw new GameNotFoundException("Game not found with id: " + id);
        }
        gameRepository.deleteById(id);
    }

    @PostConstruct
    public void seedGames() {
        if (gameRepository.count() == 0) {
            List<Game> games = Arrays.asList(
                    new Game(null, "Game 1", "Action", 29.99),
                    new Game(null, "Game 2", "Adventure", 49.99),
                    new Game(null, "Game 3", "RPG", 39.99),
                    new Game(null, "Game 4", "Puzzle", 19.99),
                    new Game(null, "Game 5", "Strategy", 34.99),
                    new Game(null, "Game 6", "Shooter", 59.99),
                    new Game(null, "Game 7", "Simulation", 29.99),
                    new Game(null, "Game 8", "Horror", 44.99),
                    new Game(null, "Game 9", "Sports", 54.99),
                    new Game(null, "Game 10", "Racing", 24.99)
            );
            gameRepository.saveAll(games);
        }
    }
}
