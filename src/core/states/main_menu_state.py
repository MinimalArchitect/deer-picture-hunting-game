from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import GameState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class MainMenuState(GameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        self.center_x = WINDOW_WIDTH // 2
        button_x = self.center_x - DefaultButtonConfig.default_width // 2

        self.main_buttons = [
            Button("Single Player", button_x, 150),
            Button("Host Game", button_x, 220),
            Button("Join Game", button_x, 290),
            Button("Options", button_x, 360),
            Button("High Scores", button_x, 430),
            Button("Exit", button_x, 500)
        ]

    def enter(self) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        assert self.game_context.playing_context is None

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        # Draw title
        title_text = GameFont.heading1_font.render("Deer Picture Hunting", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(self.center_x, 80))
        self.screen.blit(title_text, title_rect)

        # Draw version text
        version_text = GameFont.version_font.render("2D Grid-Based Version", True, Color.BLACK)
        version_rect = version_text.get_rect(center=(self.center_x, 120))
        self.screen.blit(version_text, version_rect)

        # Draw buttons
        for button in self.main_buttons:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.main_buttons):
                    if button.is_clicked(mouse_pos):
                        if i == 0:  # Single Player
                            self._transition_request = GameState.LEVEL_SELECTION_MENU
                        elif i == 1:  # Host Game
                            self._transition_request = GameState.COMING_SOON
                        elif i == 2:  # Join Game
                            self._transition_request = GameState.COMING_SOON
                        elif i == 3:  # Options
                            self._transition_request = GameState.OPTIONS_MENU
                        elif i == 4:  # High Scores
                            self._transition_request = GameState.HIGH_SCORE_MENU
                        elif i == 5:  # Exit
                            self.game_context.is_running = False