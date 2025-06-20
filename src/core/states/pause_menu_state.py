import time
from typing import List

import pygame
from pygame import Surface

from src.core.game_context import GameContext, PlayingContext
from src.core.game_state import GameState
from src.core.states.playing_state import PlayingState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT


class PauseMenuState(GameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((0, 0, 0, 150))  # Semi-transparent black

        self.continue_button = Button("Continue", center_x, 200)
        self.main_menu_button = Button("Main Menu", center_x, 270)
        self.exit_button = Button("Exit", center_x, 340)

    def enter(self) -> None:
        assert self.game_context.playing_context is not None

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        if self.game_context.playing_context is None:
            return

        PlayingState.draw_game(self.screen, self.game_context)

        # PauseMenuState.draw_game(self.screen, self.game_context)

        self.screen.blit(self.overlay, (0, 0))

        for button in [self.continue_button, self.main_menu_button, self.exit_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    @staticmethod
    def draw_game(screen: Surface, game_context: GameContext) -> None:
        playing_context = game_context.playing_context

        # Draw Game
        playing_context.map.draw(screen)

        for deer in playing_context.deer:
            deer.draw(screen)

        playing_context.player.draw(screen)

        # Draw UI
        score_text = GameFont.text_font.render(f"Score: {playing_context.score}", True, Color.BLACK)
        screen.blit(score_text, (10, 10))

        time_text = GameFont.text_font.render(f"Time: {int(playing_context.time_left)}s", True, Color.BLACK)
        screen.blit(time_text, (WINDOW_WIDTH - time_text.get_width() - 10, 10))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
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
        self._transition_request = GameState.MAIN_MENU

    def continue_game(self):
        self.game_context.last_time = time.time()
        self._transition_request = GameState.PLAYING
