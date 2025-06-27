from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import BaseGameState, GameState
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT


class GameOverState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        self.center_y = WINDOW_HEIGHT // 2

    def get_enum_value(self) -> GameState:
        return GameState.MENU_GAME_OVER

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is not None

    def exit(self) -> None:
        self.game_context.playing_context = None

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        game_over_text = GameFont.heading1_font.render("GAME OVER", True, Color.BLACK)
        game_over_text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(game_over_text, game_over_text_rect)

        final_score_text = GameFont.heading1_font.render(f"Final Score: {self.game_context.playing_context.score}", True, Color.BLACK)
        final_score_text_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(final_score_text, final_score_text_rect)

        instruction_text = GameFont.text_font.render("Press any key to continue", True, Color.BLACK)
        instruction_text_rect = final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
        self.screen.blit(instruction_text, instruction_text_rect)

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self._transition_request = GameState.MENU_MAIN
