from typing import List

import pygame
import validators
from validators import ValidationError

from src.core.game_context import GameContext, MultiPlayerContext
from src.core.game_state import BaseGameState, GameState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class ServerSelectionMenuState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.server_host = ""

        # Rectangle position and size
        self.rect_width, self.rect_height = 220, 50
        self.rect_x, self.rect_y = WINDOW_WIDTH // 2 - self.rect_width // 2, 250
        self.border_thickness = 4

        self.back_button = Button("Back", center_x - DefaultButtonConfig.default_width // 2 - 10, 400)
        self.join_button = Button("Join", center_x + DefaultButtonConfig.default_width // 2 + 10, 400)
        self.join_button.disable()

    def get_enum_value(self) -> GameState:
        return GameState.MENU_SERVER_SELECTION

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        # Render input field
        ## Draw black border (thicker rectangle)
        pygame.draw.rect(
            self.screen, (0, 0, 0),
            (self.rect_x, self.rect_y, self.rect_width, self.rect_height)
        )

        ## Draw white rectangle (inside, so border is visible)
        pygame.draw.rect(
            self.screen, (255, 255, 255),
            (
                self.rect_x + self.border_thickness,
                self.rect_y + self.border_thickness,
                self.rect_width - 2 * self.border_thickness,
                self.rect_height - 2 * self.border_thickness
            )
        )

        ## Render input text
        text = GameFont.text_font.render(self.server_host, True, Color.BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 275))
        self.screen.blit(text, text_rect)

        for button in [self.join_button, self.back_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MENU_MAIN
                if self.join_button.is_clicked(mouse_pos):
                    self.game_context.playing_context = MultiPlayerContext(difficulty=0)
                    self.game_context.playing_context.server_host = (self.server_host, 12345)
                    self._transition_request = GameState.MENU_PLAYER_SELECTION

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.server_host = self.server_host[:-1]
                elif len(self.server_host) < 50:
                    self.server_host += event.unicode

                try:
                    if not self.server_host.isdigit() and validators.hostname(self.server_host, may_have_port=False, consider_tld=True, maybe_simple=True):
                        self.join_button.enable()
                    else:
                        self.join_button.disable()
                except ValidationError:
                    self.join_button.disable()
