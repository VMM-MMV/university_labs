package crazy.demo.game;

import org.springframework.stereotype.Service;

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

    public List<Game> getAllGames() {
        return gameRepository.findAll();
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
}
