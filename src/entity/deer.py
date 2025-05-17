import random

import pygame

from src.entity.game_object import GameObject
from src.util.color import BROWN
from src.util.config import GRID_SIZE, GRID_WIDTH, GRID_HEIGHT


class Deer(GameObject):
    """Deer that player photographs"""

    def __init__(self, x, y, deer_type="NORMAL"):
        super().__init__(x, y)
        self.deer_type = deer_type
        self.photographed = False
        self.alert_level = 0  # 0-10, higher means more likely to flee

    def draw(self, surface):
        # Draw deer as brown circle
        center_x = self.x * GRID_SIZE + GRID_SIZE // 2
        center_y = self.y * GRID_SIZE + GRID_SIZE // 2
        pygame.draw.circle(surface, BROWN, (center_x, center_y), GRID_SIZE // 2)

    def update(self, player, game_map):
        """Update deer behavior based on player position"""
        # Calculate distance to player
        distance = abs(self.x - player.x) + abs(self.y - player.y)  # Manhattan distance

        # If player is close, become more alert
        if distance < 5:
            self.alert_level += 2
        else:
            self.alert_level = max(0, self.alert_level - 1)  # Calm down over time

        # If very alert, try to move away from player
        if self.alert_level > 5:
            self.flee(player, game_map)
        else:
            # Random movement (25% chance)
            if random.random() < 0.25:
                self.random_move(game_map)

    def flee(self, player, game_map):
        """Move away from player"""
        # Determine direction away from player
        dx = 1 if self.x < player.x else -1
        dy = 1 if self.y < player.y else -1

        # Try to move in that direction
        possible_moves = [
            (-dx, 0),  # Horizontal away
            (0, -dy),  # Vertical away
            (-dx, -dy),  # Diagonal away
            (0, 0)  # Stay put
        ]

        # Shuffle to avoid predictable patterns
        random.shuffle(possible_moves)

        # Try each move until we find a valid one
        for move_dx, move_dy in possible_moves:
            new_x = self.x + move_dx
            new_y = self.y + move_dy

            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                    game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
                self.x = new_x
                self.y = new_y
                break

    def random_move(self, game_map):
        """Move in a random direction"""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            new_x = self.x + dx
            new_y = self.y + dy

            if (0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and
                    game_map.get_cell(new_x, new_y) not in ["TREE", "ROCK"]):
                self.x = new_x
                self.y = new_y
                break
