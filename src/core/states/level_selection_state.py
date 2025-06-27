from typing import List

import pygame

from src.core.game_context import GameContext, SinglePlayerContext
from src.core.game_state import BaseGameState, GameState
from src.ui.button import Button, DefaultButtonConfig
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class LevelSelectionState(BaseGameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        columns = 5
        spacing = 10
        button_width = 100
        button_height = 40
        start_x = WINDOW_WIDTH // 2 - ((columns * button_width) + (columns - 1) * spacing) // 2
        start_y = 180
        total_levels = 20

        button_center_x = WINDOW_WIDTH // 2 - DefaultButtonConfig.default_width // 2
        self.back_button = Button(
            "Back",
            button_center_x,
            start_y + ((total_levels // columns) + 2) * (button_height + spacing)
        )

        self.level_buttons = []
        for level in range(total_levels):
            row = level // columns
            col = level % columns
            level_key = str(level + 1)
            score = self.game_context.level_scores.get(level_key, None)
            self.level_buttons.append(Button(
                f"{level + 1}",
                start_x + col * (button_width + spacing), start_y + row * (button_height + spacing),
                button_width,
                button_height,
                Color.BUTTON_DONE if score is not None else Color.BUTTON
            ))

    def get_enum_value(self) -> GameState:
        return GameState.MENU_LEVEL_SELECTION

    def enter(self, old_state: GameState | None) -> None:
        assert self.game_context.playing_context is None

    def exit(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def render(self) -> None:
        title_text = GameFont.heading1_font.render("Choose Level", True, Color.BLACK)
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 100))

        for button in self.level_buttons + [self.back_button]:
            button.draw(self.screen, button.check_hover(pygame.mouse.get_pos()))

    def handle_events(self, events: List[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.back_button.is_clicked(mouse_pos):
                    self._transition_request = GameState.MENU_MAIN
                for level, button in enumerate(self.level_buttons, 1):
                    if button.is_clicked(mouse_pos):
                        self.game_context.playing_context = SinglePlayerContext(level=level)
                        self._transition_request = GameState.SINGLEPLAYER_PLAYING
