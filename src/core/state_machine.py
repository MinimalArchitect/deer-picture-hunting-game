"""
State machine for managing game states and transitions.
Provides centralized state management and clean transitions.
"""

from typing import Type

import pygame

from src.core.game_context import GameContext
from src.core.game_state import BaseGameState, GameState
from src.core.states import *
from src.core.states.address_bind_failed_state import AddressBindFailedState
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
        self._old_state = None
        self._current_state: BaseGameState = StateMachine.get_game_state_from_name(GameState.MENU_MAIN)(game_context)
        self._current_state.enter(self._old_state)

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
                break
        self._current_state.handle_events(events)
        self._current_state.update(self._passed_time)
        self._game_context.screen.fill(Color.BACKGROUND)
        self._current_state.render()

        next_state = StateMachine.get_game_state_from_name(self._current_state.get_transition_request())

        if next_state:
            self._old_state = self._current_state.get_enum_value()
            self._current_state.exit()
            self._current_state = next_state(self._game_context)
            pygame.event.clear()
            self._current_state.enter(self._old_state)

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
    def get_game_state_from_name(name: GameState) -> Type[BaseGameState] | None:
        match name:
            case GameState.SINGLEPLAYER_PLAYING:
                return SinglePlayerPlayingState
            case GameState.MENU_GAME_OVER:
                return GameOverState
            case GameState.MENU_PAUSE:
                return PauseMenuState
            case GameState.MENU_MAIN:
                return MainMenuState
            case GameState.MENU_LEVEL_SELECTION:
                return LevelSelectionState
            case GameState.MENU_HIGH_SCORE:
                return HighScoreMenuState
            case GameState.MENU_OPTIONS:
                return OptionsMenuState
            case GameState.MENU_COMING_SOON:
                return ComingSoonMenuState
            case GameState.MENU_SERVER_SELECTION:
                return ServerSelectionMenuState
            case GameState.MENU_PLAYER_SELECTION:
                return PlayerSelectionMenuState
            case GameState.MENU_ERROR_ADDRESS_BIND:
                return AddressBindFailedState
        return None
