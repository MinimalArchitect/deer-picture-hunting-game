from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import GameState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class ComingSoonMenuState(GameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.back_button = Button("Back", center_x, 400)

    def enter(self) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        assert self.game_context.playing_context is None

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        # "Coming soon" message
        text = GameFont.heading1_font.render("Coming Soon", True, Color.BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(text, text_rect)

        # Back button
        self.back_button.draw(self.screen, self.back_button.check_hover(pygame.mouse.get_pos()))

    def handle_event(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MAIN_MENU
