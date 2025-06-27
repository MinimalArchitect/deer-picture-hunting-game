import json
import os
import random
import time
from typing import Tuple

import pygame
from pygame.time import Clock

from src.core.game_map import GameMap, GridType
from src.entity.deer import Deer
from src.entity.player import Player, PlayerColor
from src.networking.listener import GameServer, GameClient
from src.util.config import GRID_WIDTH, GRID_HEIGHT


def _clamp(minimum, value, maximum):
    return max(minimum, min(value, maximum))


class PlayingContext:

    def __init__(self, level: int, map: GameMap):
        self.level = level
        self.map = map

        # Game state
        self.score = 0
        self.time_left = 60  # 60 seconds
        self.last_time = time.time()

    def _place_in_empty_cell(self, object_class):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.map.get_cell(x, y) == GridType.EMPTY:
                return object_class(x, y)

    def _place_hunter_in_empty_cell(self, clothes_color: PlayerColor):
        """Place a new object in a random empty cell"""
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)

            if self.map.get_cell(x, y) == GridType.EMPTY:
                return Player(x, y, clothes_color)


class MultiPlayerContext(PlayingContext):
    def __init__(self, difficulty: int):
        """Set up the game objects when starting a new game"""
        # Playing GameState
        self.difficulty = difficulty
        level = _clamp(0, self.difficulty + random.randint(-1, +1), 20)
        super().__init__(level, GameMap(level=level))
        self.server: GameServer | None = None
        self.client: GameClient | None = None

        self.server_host: Tuple[str, int] | None = None

        # Place the player in an empty cell
        self.players = [self._place_hunter_in_empty_cell(PlayerColor.GREEN)]

        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self._place_in_empty_cell(Deer))


class SinglePlayerContext(PlayingContext):
    def __init__(self, level: int):
        """Set up the game objects when starting a new game"""
        # Playing GameState
        super().__init__(level, GameMap(level=level))

        # Place the player in an empty cell
        self.player = self._place_hunter_in_empty_cell(PlayerColor.YELLOW)

        # Create deer
        self.deer = []
        for _ in range(10):  # 10 deer
            self.deer.append(self._place_in_empty_cell(Deer))


class GameContext:
    def __init__(self, screen: pygame.Surface, clock: Clock) -> None:
        self.screen = screen
        self.clock = clock
        self.is_running = True

        # Manually set the framerate with this
        self.frame_rate = 30

        # Configuration
        self.is_sound_enabled = True

        self.playing_context: SinglePlayerContext | MultiPlayerContext | None = None

        # Game objects will be initialized when starting the game
        self.level_scores = {}  # {level_number: highest_score}
        self.score_file = "level_scores.json"
        self.load_scores()

    def save_scores(self):
        try:
            with open(self.score_file, "w") as f:
                # Ensure keys are strings for JSON compatibility
                json.dump({str(k): v for k, v in self.level_scores.items()}, f)
        except Exception as e:
            print("Error saving scores:", e)

    def load_scores(self):
        self.level_scores = {}
        if os.path.exists(self.score_file):
            try:
                with open(self.score_file, "r") as f:
                    self.level_scores = json.load(f)
            except Exception as e:
                print("Error loading scores:", e)

    def remove_scores(self):
        self.level_scores = {}
        if os.path.exists(self.score_file):
            try:
                os.remove(self.score_file)
            except Exception as e:
                print("Error resetting score file:", e)
