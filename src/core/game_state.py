"""
Abstract base class for all game states.
Defines the interface that all states must implement.
"""

from abc import ABC, abstractmethod
from typing import List

import pygame

from src.core.game_context import GameContext


class GameState(ABC):
    """
    Abstract base class for all game states.
    
    Each state represents a distinct mode of the game (menu, playing, paused, etc.)
    and handles its own logic, rendering, and events.
    """
    #Enum for game states
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    MAIN_MENU = "main_menu"
    LEVEL_SELECTION_MENU = "level_selection"
    HIGH_SCORE_MENU = "high_score_menu"
    OPTIONS_MENU = "options_menu"
    COMING_SOON = "coming_soon"

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
        self._transition_request: str | None = None

    @abstractmethod
    def enter(self) -> None:
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
            
        Returns:
            Name of state to transition to, or None to stay in current state
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
    def handle_event(self, events: List[pygame.event.Event]) -> None:
        """
        Handle a pygame event.
        
        Args:
            events: List of pygame events to handle
        """
        pass

    def get_transition_request(self) -> str | None:
        """
        Returns:
            Name of state to transition to from enum, or None to stay in the current state
        """
        return self._transition_request