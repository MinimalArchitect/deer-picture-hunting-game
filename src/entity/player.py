import math
import random
import time

import pygame

from src.core.game_map import GridType
from src.entity.game_object import GameObject
from src.util.color import Color
from src.util.texture import Texture
from src.util.config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT

class Direction:
    """Player direction"""
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

class Player(GameObject):
    """Player character"""

    def __init__(self, x, y, clothes_color):
        super().__init__(x, y)
        self.direction = Direction.UP
        self.photos_taken = 0
        self.spawn_time = time.time()  # Store the time when player is created
        self.clothes_color = clothes_color

    def draw(self, surface):
        # Draw player pointing in direction
        pos = (self.x * GRID_SIZE, self.y * GRID_SIZE)

        match self.direction:
            case Direction.UP:
                surface.blit(Texture.hunter_back, pos)
            case Direction.DOWN:
                surface.blit(Texture.hunter_front, pos)
            case Direction.LEFT:
                surface.blit(Texture.hunter_left, pos)
            case Direction.RIGHT:
                surface.blit(Texture.hunter_right, pos)

        # Highlight the player with pulsing color of the hunter's clothes glow for 3 seconds
        if time.time() - self.spawn_time < 3:
            pulse_alpha = int(100 + 50 * math.sin((time.time() - self.spawn_time) * 6))
            highlight = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            highlight.fill((*self.clothes_color, pulse_alpha))
            surface.blit(highlight, pos)

    def move(self, dx, dy, game_map):
        """Try to move in the specified direction"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if new position is valid
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                game_map.get_cell(new_x, new_y) not in [GridType.TREE, GridType.ROCK]):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def take_photo(self, game_map, deer_list):
        """Take a photo in the direction the player is facing"""
        x, y = self.x, self.y

        # Direction vectors
        match self.direction:
            case Direction.UP:
                dx, dy = 0, -1
            case Direction.DOWN:
                dx, dy = 0, 1
            case Direction.LEFT:
                dx, dy = -1, 0
            case Direction.RIGHT:
                dx, dy = 1, 0

        # Track how far the photo "travels"
        photo_range = 10  # How far the photo can see

        # Check each cell in the photo's path
        deer_photographed = []
        for i in range(1, photo_range + 1):
            check_x = x + dx * i
            check_y = y + dy * i

            # Stop if we hit a boundary
            if not (0 <= check_x < GRID_WIDTH and 0 <= check_y < GRID_HEIGHT):
                break

            # Stop if we hit a solid obstacle
            if game_map.get_cell(check_x, check_y) in ["TREE", "ROCK"]:
                break

            # Check if we see a deer
            for deer in deer_list:
                if deer.x == check_x and deer.y == check_y:
                    deer_photographed.append(deer)

            # In bushes, reduce visibility (50% chance to continue)
            # TODO: Check in group if we want 'deterministic' photo behaviour
            if game_map.get_cell(check_x, check_y) == "BUSH" and random.random() < 0.5:
                break

        # Return any deer we photographed
        return deer_photographed