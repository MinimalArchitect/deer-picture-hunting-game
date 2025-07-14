import random

from src.core.config import GameServerConfig
from src.core.enum import Tile
from src.core.type import Position
from src.util.predefined_levels import LEVELS


class GameMap:
    def __init__(self, level: int) -> None:
        """
        Precondition:
            - GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL

        Postcondition:
            - Initializes map grid with tiles from predefined LEVELS
        """
        assert GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL
        self._level = level
        self._grid: list[list[Tile]] = []
        self._clear()
        self.load_map_from_file(self._level)

    def load_map_from_file(self, level: int) -> None:
        """
        Precondition:
            - GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL

        Postcondition:
            - self._grid is filled with tiles according to LEVELS[level]
        """
        assert GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL
        layout = LEVELS.get(level, LEVELS[max(LEVELS.keys())])
        for y, row in enumerate(layout):
            for x, character in enumerate(row):
                assert 0 <= x < GameServerConfig.GRID_WIDTH and 0 <= y < GameServerConfig.GRID_HEIGHT
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
        Postcondition:
            - Initializes self._grid to a 2D grid filled with Tile.EMPTY
        """
        self._grid = [[Tile.EMPTY for _ in range(GameServerConfig.GRID_HEIGHT)] for _ in range(GameServerConfig.GRID_WIDTH)]

    def get_tile(self, position: Position) -> Tile:
        """
        Precondition:
            - 0 <= position.x < GameServerConfig.GRID_WIDTH
            - 0 <= position.y < GameServerConfig.GRID_HEIGHT

        Postcondition:
            - Returns the tile at the specified position
        """
        assert 0 <= position.x < GameServerConfig.GRID_WIDTH and 0 <= position.y < GameServerConfig.GRID_HEIGHT
        return self._grid[position.x][position.y]

    def get_empty_tile(self) -> Position:
        """
        Postcondition:
            - Returns a random position on the grid where the tile is Tile.EMPTY
        """
        while True:
            position = Position(
                random.randint(0, GameServerConfig.GRID_WIDTH - 1),
                random.randint(0, GameServerConfig.GRID_HEIGHT - 1)
            )

            if self.get_tile(position) == Tile.EMPTY:
                return position
