import math
import time
from enum import IntEnum, auto, StrEnum
from typing import List

import pygame

from src.core.game_map import GridType
from src.entity.deer import Deer
from src.entity.game_object import GameObject
from src.util.color import Color
from src.util.config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT
from src.util.texture import Texture


class Direction(IntEnum):
    """Player direction"""
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class PlayerColor(StrEnum):
    """Player color"""
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"


class Player(GameObject):
    """Player character"""

    def __init__(self, x, y, clothes_color: PlayerColor = PlayerColor.GREEN):
        super().__init__(x, y)
        self.direction = Direction.UP
        self.photos_taken = 0
        self.spawn_time = time.time()  # Store the time when player is created
        self.clothes_color = clothes_color

        self.texture_back = None
        self.texture_front = None
        self.texture_left = None
        self.texture_right = None
        self.color_fill = None

        match clothes_color:
            case PlayerColor.RED:
                self.texture_back = Texture.hunter_red_back
                self.texture_front = Texture.hunter_red_front
                self.texture_right = Texture.hunter_red_right
                self.texture_left = Texture.hunter_red_left
                self.color_fill = Color.RED
            case PlayerColor.BLUE:
                self.texture_back = Texture.hunter_blue_back
                self.texture_front = Texture.hunter_blue_front
                self.texture_right = Texture.hunter_blue_right
                self.texture_left = Texture.hunter_blue_left
                self.color_fill = Color.BLUE
            case PlayerColor.GREEN:
                self.texture_back = Texture.hunter_green_back
                self.texture_front = Texture.hunter_green_front
                self.texture_right = Texture.hunter_green_right
                self.texture_left = Texture.hunter_green_left
                self.color_fill = Color.LIGHT_GREEN
            case PlayerColor.YELLOW:
                self.texture_back = Texture.hunter_yellow_back
                self.texture_front = Texture.hunter_yellow_front
                self.texture_right = Texture.hunter_yellow_right
                self.texture_left = Texture.hunter_yellow_left
                self.color_fill = Color.YELLOW

    def draw(self, surface):
        # Draw player pointing in direction
        pos = (self.x * GRID_SIZE, self.y * GRID_SIZE)

        match self.direction:
            case Direction.UP:
                surface.blit(self.texture_back, pos)
            case Direction.DOWN:
                surface.blit(self.texture_front, pos)
            case Direction.LEFT:
                surface.blit(self.texture_left, pos)
            case Direction.RIGHT:
                surface.blit(self.texture_right, pos)

        # Highlight the player with pulsing color of the hunter's clothes glow for 3 seconds
        if time.time() - self.spawn_time < 3:
            pulse_alpha = int(100 + 50 * math.sin((time.time() - self.spawn_time) * 6))
            highlight = pygame.Surface((GRID_SIZE, GRID_SIZE), pygame.SRCALPHA)
            highlight.fill((*self.color_fill, pulse_alpha))
            surface.blit(highlight, pos)

    def move(self, dx, dy, game_map, deer_list: List[Deer]):
        """Try to move in the specified direction"""
        new_x = self.x + dx
        new_y = self.y + dy

        new_hunter_position = (new_x, new_y)

        def is_deer_at_position(deer_list, position):
            for deer in deer_list:
                deer_position = (deer.x, deer.y)
                if deer_position == position:
                    return True
            return False

        # Check if new position is valid
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                game_map.get_cell(new_x, new_y) not in [GridType.TREE, GridType.ROCK] and
                not is_deer_at_position(deer_list, new_hunter_position)):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def take_photo(self, game_map, deer_list):
        """Take a photo in the direction the player is facing"""
        x, y = self.x, self.y

        # Direction vectors
        dx, dy = 0, 0
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
            if game_map.get_cell(check_x, check_y) in [GridType.TREE, GridType.ROCK, GridType.BUSH]:
                break

            # Check if we see a deer
            for deer in deer_list:
                if deer.x == check_x and deer.y == check_y:
                    deer_photographed.append(deer)

        # Return any deer we photographed
        return deer_photographed