"""
State machine for managing game states and transitions.
Provides centralized state management and clean transitions.
"""

from typing import Type

import pygame

from src.core.game_context import GameContext
from src.core.game_state import GameState
from src.core.states import GameOverState, PlayingState, MainMenuState, PauseMenuState, LevelSelectionState, HighScoreMenuState
from src.core.states.coming_soon_menu_state import ComingSoonMenuState
from src.core.states.options_menu_state import OptionsMenuState
from src.util.color import Color


class StateMachine:
    """
    Manages game states and handles transitions between them.
    
    Provides a centralized way to manage state changes, ensuring
    proper cleanup and initialization during transitions.
    """

    def __init__(self, game_context: GameContext):
        """
        Initialize the state machine.
        
        Args:
            game_context: Reference to the main Game instance
        """
        self._game_context = game_context
        self._current_state: GameState = StateMachine.get_game_state_from_name(GameState.MAIN_MENU)(game_context)
        self._current_state.enter()

        self._is_running = True

        self._passed_time = 0  # in ms

    def update(self) -> None:
        """
        Update the current state.
        """
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self._game_context.is_running = False

        self._current_state.handle_event(events)
        self._current_state.update(self._passed_time)
        self._game_context.screen.fill(Color.BACKGROUND)
        self._current_state.render()

        next_state = StateMachine.get_game_state_from_name(self._current_state.get_transition_request())

        if next_state:
            self._current_state.exit()
            self._current_state = next_state(self._game_context)
            pygame.event.clear()
            self._current_state.enter()

        pygame.display.flip()
        self._passed_time = self._game_context.clock.tick(self._game_context.frame_rate)

    def shutdown(self) -> None:
        """Shutdown the state machine and clean up."""
        if self._current_state:
            self._current_state.exit()
            self._current_state = None
        print("State machine shutdown")

    def is_running(self) -> bool:
        return self._game_context.is_running

    @staticmethod
    def get_game_state_from_name(name: str) -> Type[GameState] | None:
        if name == GameState.PLAYING:
            return PlayingState
        elif name == GameState.PAUSED:
            return PauseMenuState
        elif name == GameState.GAME_OVER:
            return GameOverState
        elif name == GameState.MAIN_MENU:
            return MainMenuState
        elif name == GameState.LEVEL_SELECTION_MENU:
            return LevelSelectionState
        elif name == GameState.HIGH_SCORE_MENU:
            return HighScoreMenuState
        elif name == GameState.OPTIONS_MENU:
            return OptionsMenuState
        elif name == GameState.COMING_SOON:
            return ComingSoonMenuState
        else:
            return None
