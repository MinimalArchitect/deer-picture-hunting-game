from typing import List

import pygame

from src.core.game_context import GameContext, MultiPlayerContext
from src.core.game_state import BaseGameState, GameState
from src.networking.listener import GameServer, GameClient
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class PlayerSelectionMenuState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2

        self.back_button = Button("Back", center_x, 400)

    def get_enum_value(self) -> GameState:
        return GameState.MENU_PLAYER_SELECTION

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is not None

        playing_context: MultiPlayerContext = self.game_context.playing_context

        try:
            if old_state == GameState.MENU_MAIN:
                self.game_context.playing_context.server = GameServer(playing_context.server_host)
            elif old_state == GameState.MENU_SERVER_SELECTION:
                self.game_context.playing_context.client = GameClient(playing_context.server_host)
        except OSError:
            self._transition_request = GameState.MENU_ERROR_ADDRESS_BIND
            self.game_context.playing_context = None

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        playing_context: MultiPlayerContext = self.game_context.playing_context
        if self.game_context.playing_context is None:
            return

        if playing_context.server is not None:
            self.game_context.playing_context.server.Pump()
        else:
            self.game_context.playing_context.client.Pump()
        pass

    def render(self) -> None:
        # "Coming soon" message
        text = GameFont.heading1_font.render("Coming Soon", True, Color.BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(text, text_rect)

        # Back button
        self.back_button.draw(self.screen, self.back_button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MENU_MAIN
                    self.game_context.playing_context = None
