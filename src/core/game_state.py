"""
Abstract base class for all game states.
Defines the interface that all states must implement.
"""

from abc import ABC, abstractmethod
from enum import auto, IntEnum
from typing import List

import pygame

from src.core.game_context import GameContext


class GameState(IntEnum):
    SINGLEPLAYER_PLAYING = auto()
    MULTIPLAYER_PLAYING = auto()
    MENU_GAME_OVER = auto()
    MENU_PAUSE = auto()
    MENU_MAIN = auto()
    MENU_LEVEL_SELECTION = auto()
    MENU_HIGH_SCORE = auto()
    MENU_OPTIONS = auto()
    MENU_COMING_SOON = auto()
    MENU_SERVER_SELECTION = auto()
    MENU_PLAYER_SELECTION = auto()
    MENU_ERROR_ADDRESS_BIND = auto()


class BaseGameState(ABC):
    """
    Abstract base class for all game states.
    
    Each state represents a distinct mode of the game (menu, playing, paused, etc.)
    and handles its own logic, rendering, and events.
    """

    # Enum for game states

    def __init__(self, game_context: GameContext):
        """
        Initialize the state with access to the game context.
        
        Args:
            game_context: Reference to the main Game instance for shared resources
        """
        # Game Data
        self.game_context = game_context
        self.screen = game_context.screen
        self.clock = game_context.clock

        # Transition Data
        self._transition_request: GameState | None = None

    @abstractmethod
    def enter(self, old_state: GameState | None) -> None:
        """
        Called when entering this state.
        """
        pass

    @abstractmethod
    def exit(self) -> None:
        """
        Called when leaving this state.
        """
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        """
        Update the state logic.
        
        Args:
            dt: Delta time since last update in seconds
        """
        pass

    @abstractmethod
    def render(self) -> None:
        """
        Render the state to the screen.
        This method should handle all drawing for this state.
        """
        pass

    @abstractmethod
    def handle_events(self, events: List[pygame.event.Event]) -> None:
        """
        Handle a pygame event.
        
        Args:
            events: List of pygame events to handle
        """
        pass

    def get_transition_request(self) -> GameState | None:
        """
        Returns:
            Name of state to transition to from enum, or None to stay in the current state
        """
        return self._transition_request

    @abstractmethod
    def get_enum_value(self) -> GameState:
        pass
