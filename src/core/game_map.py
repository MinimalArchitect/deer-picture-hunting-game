import random

from src.util.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE
from src.util.predefined_levels import LEVELS
from src.util.texture import Texture


class GridType:
    """Types of grid cells"""
    EMPTY = "EMPTY"
    TREE = "TREE"
    ROCK = "ROCK"
    BUSH = "BUSH"


class GameMap:
    """Represents the game environment"""

    def __init__(self):
        self.grid = [[GridType.EMPTY for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def generate_random_map(self):
        """Generate a random map with trees, rocks, bushes"""
        # Add trees (20% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.2)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.grid[x][y] = GridType.TREE

        # Add rocks (10% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.1)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == GridType.EMPTY:
                self.grid[x][y] = GridType.ROCK

        # Add bushes (15% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.15)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == GridType.EMPTY:
                self.grid[x][y] = GridType.BUSH

    def generate_predefined_map(self, level=1):
        """Load predefined level layout"""
        self.clear()
        layout = LEVELS.get(level, LEVELS[max(LEVELS.keys())])
        for y, row in enumerate(layout):
            for x, char in enumerate(row):
                if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
                    match char:
                        case 'T':
                            self.grid[x][y] = GridType.TREE
                        case 'R':
                            self.grid[x][y] = GridType.ROCK
                        case 'B':
                            self.grid[x][y] = GridType.BUSH
                        case _:
                            self.grid[x][y] = GridType.EMPTY

    def clear(self):
        self.grid = [[GridType.EMPTY for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def get_cell(self, x, y):
        """Get the type of cell at the given coordinates"""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.grid[x][y]
        return None

    def draw(self, surface):
        """Draw the map"""
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                self._draw_grid_cell(surface, x, y)

    def _draw_grid_cell(self, surface, x, y):
        pos = (x * GRID_SIZE, y * GRID_SIZE)
        # Fill the cell with grass first
        surface.blit(Texture.grass, pos)

        match self.grid[x][y]:
            case GridType.TREE:
                surface.blit(Texture.tree, pos)
            case GridType.ROCK:
                surface.blit(Texture.rock, pos)
            case GridType.BUSH:
                surface.blit(Texture.bush, pos)
