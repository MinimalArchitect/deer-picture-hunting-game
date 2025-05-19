import pygame

from src.ui.button import Button
from src.util.color import Color
from src.util.config import WINDOW_WIDTH


class MenuType:
    MAIN = "main"
    OPTIONS = "options"
    HIGH_SCORES = "high_scores"


class Menu:
    """Game menu system"""

    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.current_menu = MenuType.MAIN

        # Create buttons for main menu
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2

        self.main_buttons = [
            Button(center_x, 150, button_width, button_height, "Single Player", Color.BUTTON, Color.BUTTON_HOVER),
            Button(center_x, 220, button_width, button_height, "Host Game", Color.BUTTON, Color.BUTTON_HOVER),
            Button(center_x, 290, button_width, button_height, "Join Game", Color.BUTTON, Color.BUTTON_HOVER),
            Button(center_x, 360, button_width, button_height, "Options", Color.BUTTON, Color.BUTTON_HOVER),
            Button(center_x, 430, button_width, button_height, "High Scores", Color.BUTTON, Color.BUTTON_HOVER),
            Button(center_x, 500, button_width, button_height, "Exit", Color.BUTTON, Color.BUTTON_HOVER)
        ]

        # Load title font
        self.title_font = pygame.font.SysFont(None, 64)

        self.sound_toggle_button = Button(
            WINDOW_WIDTH // 2 - 100, 250, 200, 50,
            "Sound: On", Color.BUTTON, Color.BUTTON_HOVER
        )
        self.back_button = Button(
            WINDOW_WIDTH // 2 - 100, 320, 200, 50,
            "Back", Color.BUTTON, Color.BUTTON_HOVER
        )

    def draw_options(self, sound_enabled):
        """Draw the options menu (placeholder)"""
        # Title
        font = pygame.font.SysFont(None, 48)
        title_text = font.render("Options", True, Color.BLACK)
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_text, title_rect)

        # Update button label
        self.sound_toggle_button.text = f"Sound: {'On' if sound_enabled else 'Off'}"

        # Sound toggle button
        is_sound_hovered = self.sound_toggle_button.check_hover(pygame.mouse.get_pos())
        self.sound_toggle_button.draw(self.screen, is_sound_hovered)

        # TODO: Configure sound volume
        # TODO: Configure size of the game

        # Back button
        is_back_hovered = self.back_button.check_hover(pygame.mouse.get_pos())
        self.back_button.draw(self.screen, is_back_hovered)

        # Check clicks
        if is_sound_hovered and pygame.mouse.get_pressed()[0]:
            return "toggle_sound"
        elif is_back_hovered and pygame.mouse.get_pressed()[0]:
            self.current_menu = MenuType.MAIN
        return None

    def draw_high_scores(self):
        """Draw the high scores menu (placeholder)"""
        self.draw_coming_soon_screen("High Scores")

    def draw_coming_soon_screen(self, text: str):
        """Draw the placeholder coming soon screen"""
        # Simple "Coming soon" message and back button
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"{text}: Coming Soon", True, Color.BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(text, text_rect)

        # Back button
        back_button = Button(WINDOW_WIDTH // 2 - 100, 400, 200, 50, "Back", Color.BUTTON, Color.BUTTON_HOVER)
        is_back_button_hovered = back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(self.screen, is_back_button_hovered)

        # TODO split up drawing and behaviour

        # Check for back button click
        if is_back_button_hovered and pygame.mouse.get_pressed()[0]:
            self.current_menu = MenuType.MAIN
