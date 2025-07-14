from src.core.config import GameClientConfig
from src.core.enum import Tile
from src.util.predefined_levels import LEVELS
from src.util.texture import Texture


class GameMap:
    def __init__(self, level: int) -> None:
        """
        Initialize a game map for a given level.

        Precondition:
            - GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL

        Postcondition:
            - self._level is set to the given level
            - self._grid is populated with tiles from LEVELS[level]
        """
        assert GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL
        self._level = level
        self._grid: list[list[Tile]] = []
        self._clear()
        self.load_map_from_file(self._level)

    def load_map_from_file(self, level: int) -> None:
        """
        Load the map layout from a predefined level.

        Precondition:
            - GameClientConfig.MIN_LEVEL <= level <= GameClientConfig.MAX_LEVEL

        Postcondition:
            - self._grid is filled with tiles according to LEVELS[level]
        """
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
        """
        Clear the map to a grid filled with EMPTY tiles.

        Postcondition:
            - self._grid is a 2D list of Tile.EMPTY with correct dimensions
        """
        self._grid = [[Tile.EMPTY for _ in range(GameClientConfig.GRID_HEIGHT)] for _ in range(GameClientConfig.GRID_WIDTH)]

    def draw(self, surface):
        """
        Draw the map grid onto a surface.

        Precondition:
            - surface must be a valid drawing surface (e.g., Pygame surface)

        Postcondition:
            - Each tile's texture is drawn at its correct grid position
        """
        for x in range(GameClientConfig.GRID_WIDTH):
            for y in range(GameClientConfig.GRID_HEIGHT):
                self._draw_grid_cell(surface, x, y)

    def _draw_grid_cell(self, surface, x, y):
        """
        Draw a single grid cell (background + object).

        Precondition:
            - 0 <= x < GameClientConfig.GRID_WIDTH
            - 0 <= y < GameClientConfig.GRID_HEIGHT

        Postcondition:
            - Grass texture and optional object texture (tree, rock, bush) is drawn at (x, y)
        """
        pos = (x * GameClientConfig.TILE_SIZE, y * GameClientConfig.TILE_SIZE)
        surface.blit(Texture.grass, pos)

        match self._grid[x][y]:
            case Tile.TREE:
                surface.blit(Texture.tree, pos)
            case Tile.ROCK:
                surface.blit(Texture.rock, pos)
            case Tile.BUSH:
                surface.blit(Texture.bush, pos)
