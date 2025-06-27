import time
from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import BaseGameState, GameState
from src.core.states.singleplayer_playing_state import SinglePlayerPlayingState
from src.ui.button import Button, DefaultButtonConfig
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT


class PauseMenuState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))  # Semi-transparent black

        self.continue_button = Button("Continue", center_x, 200)
        self.main_menu_button = Button("Main Menu", center_x, 270)
        self.exit_button = Button("Exit", center_x, 340)

    def get_enum_value(self) -> GameState:
        return GameState.MENU_PAUSE

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is not None

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        if self.game_context.playing_context is None:
            return

        SinglePlayerPlayingState.draw_game(self.screen, self.game_context)

        self.screen.blit(self.overlay, (0, 0))

        for button in [self.continue_button, self.main_menu_button, self.exit_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.continue_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.continue_button.is_clicked(mouse_pos):
                    self.continue_game()
                elif self.main_menu_button.is_clicked(mouse_pos):
                    self.go_to_main_menu()
                elif self.exit_button.is_clicked(mouse_pos):
                    self.game_context.is_running = False

    def go_to_main_menu(self):
        self.game_context.playing_context = None
        self._transition_request = GameState.MENU_MAIN

    def continue_game(self):
        self.game_context.last_time = time.time()
        self._transition_request = GameState.SINGLEPLAYER_PLAYING
