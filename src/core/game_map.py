import random

import pygame

from src.util.color import GREEN
from src.util.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE


class GameMap:
    """Represents the game environment"""

    def __init__(self):
        self.grid = [["EMPTY" for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

    def generate_map(self):
        """Generate a random map with trees, rocks, bushes"""
        # Add trees (20% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.2)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            self.grid[x][y] = "TREE"

        # Add rocks (10% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.1)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == "EMPTY":
                self.grid[x][y] = "ROCK"

        # Add bushes (15% of grid)
        for _ in range(int(GRID_WIDTH * GRID_HEIGHT * 0.15)):
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if self.grid[x][y] == "EMPTY":
                self.grid[x][y] = "BUSH"

    def get_cell(self, x, y):
        """Get the type of cell at the given coordinates"""
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return self.grid[x][y]
        return None

    def draw(self, surface):
        """Draw the map"""
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)

                if self.grid[x][y] == "TREE":
                    pygame.draw.rect(surface, GREEN, rect)
                elif self.grid[x][y] == "ROCK":
                    pygame.draw.rect(surface, (100, 100, 100), rect)
                elif self.grid[x][y] == "BUSH":
                    pygame.draw.rect(surface, (144, 238, 144), rect)  # Light green
                else:
                    pygame.draw.rect(surface, (200, 255, 200), rect)  # Light grass color

                # Draw grid lines
                pygame.draw.rect(surface, (220, 220, 220), rect, 1)
