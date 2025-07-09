from src.core.config import GameClientConfig
from src.core.enum import Tile
from src.util.predefined_levels import LEVELS
from src.util.texture import Texture


class GameMap:
    def __init__(self, level: int) -> None:
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        self._level = level
        self._grid: list[list[Tile]] = []
        self._clear()
        self.load_map_from_file(self._level)

    def load_map_from_file(self, level: int) -> None:
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        layout = LEVELS.get(level, LEVELS[max(LEVELS.keys())])
        for y, row in enumerate(layout):
            for x, character in enumerate(row):
                assert 0 <= x < GameClientConfig.GRID_WIDTH and 0 <= y < GameClientConfig.GRID_HEIGHT
                match character:
                    case 'T':
                        self._grid[x][y] = Tile.TREE
                    case 'R':
                        self._grid[x][y] = Tile.ROCK
                    case 'B':
                        self._grid[x][y] = Tile.BUSH
                    case '.':
                        self._grid[x][y] = Tile.EMPTY
                    case _:
                        assert False, "unreachable"

    def _clear(self) -> None:
        self._grid = [[Tile.EMPTY for _ in range(GameClientConfig.GRID_HEIGHT)] for _ in range(GameClientConfig.GRID_WIDTH)]

    def draw(self, surface):
        for x in range(GameClientConfig.GRID_WIDTH):
            for y in range(GameClientConfig.GRID_HEIGHT):
                self._draw_grid_cell(surface, x, y)

    def _draw_grid_cell(self, surface, x, y):
        pos = (x * GameClientConfig.TILE_SIZE, y * GameClientConfig.TILE_SIZE)
        surface.blit(Texture.grass, pos)

        match self._grid[x][y]:
            case Tile.TREE:
                surface.blit(Texture.tree, pos)
            case Tile.ROCK:
                surface.blit(Texture.rock, pos)
            case Tile.BUSH:
                surface.blit(Texture.bush, pos)