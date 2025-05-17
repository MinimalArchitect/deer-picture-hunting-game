import random

import pygame

from src.entity.game_object import GameObject
from src.util.color import BLUE
from src.util.config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT


class Player(GameObject):
    """Player character"""

    def __init__(self, x, y):
        super().__init__(x, y)
        self.direction = "UP"  # UP, DOWN, LEFT, RIGHT
        self.photos_taken = 0

    def draw(self, surface):
        # Draw player as a triangle pointing in direction
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2

        if self.direction == "UP":
            points = [(center_x, center_y - 10), (center_x - 7, center_y + 5), (center_x + 7, center_y + 5)]
        elif self.direction == "DOWN":
            points = [(center_x, center_y + 10), (center_x - 7, center_y - 5), (center_x + 7, center_y - 5)]
        elif self.direction == "LEFT":
            points = [(center_x - 10, center_y), (center_x + 5, center_y - 7), (center_x + 5, center_y + 7)]
        else:  # RIGHT
            points = [(center_x + 10, center_y), (center_x - 5, center_y - 7), (center_x - 5, center_y + 7)]

        pygame.draw.polygon(surface, BLUE, points)

    def move(self, dx, dy, game_map):
        """Try to move in the specified direction"""
        new_x = self.x + dx
        new_y = self.y + dy

        # Check if new position is valid
        if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def take_photo(self, game_map, deer_list):
        """Take a photo in the direction the player is facing"""
        x, y = self.x, self.y

        # Direction vectors
        if self.direction == "UP":
            dx, dy = 0, -1
        elif self.direction == "DOWN":
            dx, dy = 0, 1
        elif self.direction == "LEFT":
            dx, dy = -1, 0
        else:  # RIGHT
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
            if game_map.get_cell(check_x, check_y) == "BUSH" and random.random() < 0.5:
                break

        # Return any deer we photographed
        return deer_photographed