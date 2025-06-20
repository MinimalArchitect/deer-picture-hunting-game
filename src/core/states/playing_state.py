import time
from typing import List

import pygame
from pygame import Surface

from src.core.game_context import GameContext
from src.core.game_state import GameState
from src.entity.player import Direction
from src.ui.gamefont import GameFont
from src.util.color import Color
from src.util.config import WINDOW_WIDTH
from src.util.sound import Sound


class PlayingState(GameState):

    def __init__(self, game_context: GameContext):
        super().__init__(game_context)
        self.previous_frame_rate = self.game_context.frame_rate

    def enter(self) -> None:
        self.game_context.frame_rate = 10

    def exit(self) -> None:
        assert self.game_context.playing_context is not None
        self.game_context.frame_rate = self.previous_frame_rate

    def update(self, dt: float) -> None:
        playing_context = self.game_context.playing_context

        # Update timer
        current_time = time.time()
        elapsed = current_time - playing_context.last_time
        playing_context.last_time = current_time

        playing_context.time_left -= elapsed
        if playing_context.time_left <= 0:
            self._transition_request = GameState.GAME_OVER

        # Update deer
        for deer in playing_context.deer:
            deer.update(playing_context.player, playing_context.map, playing_context.deer)

    def render(self) -> None:
        PlayingState.draw_game(self.screen, self.game_context)

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
        playing_context = self.game_context.playing_context

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.take_photo()
                elif event.key == pygame.K_ESCAPE:
                    self._transition_request = GameState.PAUSED

        has_moved = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            playing_context.player.direction = Direction.UP
            has_moved = playing_context.player.move(0, -1, playing_context.map, playing_context.deer)
        elif keys[pygame.K_DOWN]:
            playing_context.player.direction = Direction.DOWN
            has_moved = playing_context.player.move(0, 1, playing_context.map, playing_context.deer)
        elif keys[pygame.K_LEFT]:
            playing_context.player.direction = Direction.LEFT
            has_moved = playing_context.player.move(-1, 0, playing_context.map, playing_context.deer)
        elif keys[pygame.K_RIGHT]:
            playing_context.player.direction = Direction.RIGHT
            has_moved = playing_context.player.move(1, 0, playing_context.map, playing_context.deer)

        if has_moved and self.game_context.is_sound_enabled:
            Sound.move.play()

    def take_photo(self):
        """Player takes a photo"""
        playing_context = self.game_context.playing_context

        if self.game_context.is_sound_enabled:
            Sound.take_photo.play()

        photographed_deer = playing_context.player.take_photo(playing_context.map, playing_context.deer)
        for deer in photographed_deer:
            if not deer.photographed:
                deer.photographed = True
                playing_context.score += 1