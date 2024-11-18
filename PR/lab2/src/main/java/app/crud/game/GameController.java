package app.crud.game;

import org.springframework.data.domain.Page;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/games")
public class GameController {

    private final GameService gameService;

    public GameController(GameService gameService) {
        this.gameService = gameService;
    }

    @PostMapping
    public ResponseEntity<Game> createGame(@RequestBody Game game) {
        return ResponseEntity.ok(gameService.createGame(game));
    }

    @GetMapping
    public ResponseEntity<PageResponse<Game>> getAllGames(
            @RequestParam(defaultValue = "0") int offset,
            @RequestParam(defaultValue = "10") int limit) {

        Page<Game> gamePage = gameService.getAllGames(offset, limit);

        PageResponse<Game> response = PageResponse.<Game>builder()
                .content(gamePage.getContent())
                .totalElements(gamePage.getTotalElements())
                .offset(offset)
                .limit(limit)
                .totalPages(gamePage.getTotalPages())
                .isFirst(offset == 0)
                .isLast((offset + limit) >= gamePage.getTotalElements())
                .build();

        return ResponseEntity.ok(response);
    }

    @GetMapping("/{id}")
    public ResponseEntity<Game> getGameById(@PathVariable Long id) {
        return ResponseEntity.ok(gameService.getGameById(id));
    }

    @GetMapping("/name/{name}")
    public ResponseEntity<Game> getGameByName(@PathVariable String name) {
        return ResponseEntity.ok(gameService.getGameByName(name));
    }

    @PutMapping("/{id}")
    public ResponseEntity<Game> updateGame(@PathVariable Long id, @RequestBody Game gameDetails) {
        return ResponseEntity.ok(gameService.updateGame(id, gameDetails));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteGame(@PathVariable Long id) {
        gameService.deleteGame(id);
        return ResponseEntity.ok().build();
    }
}