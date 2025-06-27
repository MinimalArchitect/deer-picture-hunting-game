from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import BaseGameState, GameState
from src.ui.button import Button
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class HighScoreMenuState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        game_context.load_scores()

        # Back and Reset buttons
        self.back_button = Button("Back", WINDOW_WIDTH // 2 - 140, 500, 120, 40)
        self.reset_button = Button("Reset", WINDOW_WIDTH // 2 + 20, 500, 120, 40)

    def get_enum_value(self) -> GameState:
        return GameState.MENU_HIGH_SCORE

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        assert self.game_context.playing_context is None

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        # Draw title
        font = GameFont.heading1_font
        title_text = font.render("High Scores", True, Color.BLACK)
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - 130, 60))

        # Draw scores in two columns
        score_font = GameFont.text_font
        column_x = [WINDOW_WIDTH // 2 - 180, WINDOW_WIDTH // 2 + 20]
        y_start = 140
        line_spacing = 30

        for i, level in enumerate(range(1, 21)):
            col = 0 if level <= 10 else 1
            row = i if level <= 10 else i - 10
            y = y_start + row * line_spacing
            key = str(level)
            score = self.game_context.level_scores.get(key, None)
            text = f"Level {level}: {score if score is not None else '-'}"
            line = score_font.render(text, True, Color.BLACK)
            self.screen.blit(line, (column_x[col], y))

        for button in [self.back_button, self.reset_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MENU_MAIN
                elif self.reset_button.is_clicked(mouse_pos):
                    self.game_context.remove_scores()
