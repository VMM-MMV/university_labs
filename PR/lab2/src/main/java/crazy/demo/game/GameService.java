package crazy.demo.game;

import crazy.demo.exception.GameNotFoundException;
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
                    new Game(null, "Wanderlust: Echoes of Time", "Very Positive", 199.99),
                    new Game(null, "Galactic Nomads", "Mostly Positive", 129.75),
                    new Game(null, "Fables of the Forest", "Overwhelmingly Positive", 175.50),
                    new Game(null, "Neon Drift", "Very Positive", 89.99),
                    new Game(null, "Cyber Hunter: AI Awakening", "Positive", 250.00),
                    new Game(null, "Arcane Realms", "Mostly Positive", 144.99),
                    new Game(null, "Dreamweaver: A Journey Beyond", "Very Positive", 189.50),
                    new Game(null, "Monsters & Mages", "Overwhelmingly Positive", 159.99),
                    new Game(null, "Timekeeper's Paradox", "Very Positive", 220.00),
                    new Game(null, "Caverns of Chaos", "Mostly Positive", 115.25)
            );
            gameRepository.saveAll(games);
        }
    }
}
