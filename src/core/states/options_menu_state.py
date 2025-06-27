from typing import List

import pygame

from src.core.game_context import GameContext
from src.core.game_state import BaseGameState, GameState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class OptionsMenuState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.back_button = Button("Back", center_x, 400)
        self.sound_toggle_button = Button("Sound: On", center_x, 250)

    def get_enum_value(self) -> GameState:
        return GameState.MENU_OPTIONS

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        assert self.game_context.playing_context is None

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        title_text = GameFont.text_font.render("Options", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        self.sound_toggle_button.text = f"Sound: {'On' if self.game_context.is_sound_enabled else 'Off'}"

        for button in [self.sound_toggle_button, self.back_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MENU_MAIN
                if self.sound_toggle_button.is_clicked(mouse_pos):
                    self.game_context.is_sound_enabled = not self.game_context.is_sound_enabled
