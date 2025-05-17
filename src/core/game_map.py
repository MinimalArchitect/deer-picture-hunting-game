import random

import pygame

from src.util.color import GREEN
from src.util.config import GRID_HEIGHT, GRID_WIDTH, GRID_SIZE


class GameMap:
    """Represents the game environment"""

    def __init__(self):
        self.grid = [["EMPTY" for _ in range(GRID_HEIGHT)] for _ in range(GRID_WIDTH)]

        self.grass_image = pygame.image.load("assets/textures/grass.png").convert_alpha()
        self.grass_image = pygame.transform.scale(self.grass_image, (GRID_SIZE, GRID_SIZE))

        self.rock_image = pygame.image.load("assets/textures/rock.png").convert_alpha()
        self.rock_image = pygame.transform.scale(self.rock_image, (GRID_SIZE, GRID_SIZE))

        self.tree_image = pygame.image.load("assets/textures/tree.png").convert_alpha()
        self.tree_image = pygame.transform.scale(self.tree_image, (GRID_SIZE, GRID_SIZE))

        self.bush_image = pygame.image.load("assets/textures/bush.png").convert_alpha()
        self.bush_image = pygame.transform.scale(self.bush_image, (GRID_SIZE, GRID_SIZE))

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
                pos = (x * GRID_SIZE, y * GRID_SIZE)

                # Fill the whole grid with grass
                surface.blit(self.grass_image, pos)

                if self.grid[x][y] == "TREE":
                    surface.blit(self.tree_image, pos)
                elif self.grid[x][y] == "ROCK":
                    surface.blit(self.rock_image, pos)
                elif self.grid[x][y] == "BUSH":
                    surface.blit(self.bush_image, pos)
