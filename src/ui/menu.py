import pygame

from src.ui.button import Button
from src.util.color import BLACK
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

        # Define colors
        self.bg_color = (230, 240, 240)  # Light blue-gray background
        self.button_color = (180, 210, 180)  # Light green
        self.button_hover = (150, 200, 150)  # Slightly darker green

        # Create buttons for main menu
        button_width = 200
        button_height = 50
        center_x = WINDOW_WIDTH // 2 - button_width // 2

        self.main_buttons = [
            Button(center_x, 150, button_width, button_height, "Single Player", self.button_color, self.button_hover),
            Button(center_x, 220, button_width, button_height, "Host Game", self.button_color, self.button_hover),
            Button(center_x, 290, button_width, button_height, "Join Game", self.button_color, self.button_hover),
            Button(center_x, 360, button_width, button_height, "Options", self.button_color, self.button_hover),
            Button(center_x, 430, button_width, button_height, "High Scores", self.button_color, self.button_hover),
            Button(center_x, 500, button_width, button_height, "Exit", self.button_color, self.button_hover)
        ]

        # Load title font
        self.title_font = pygame.font.SysFont(None, 64)

    def draw_options(self):
        """Draw the options menu (placeholder)"""
        self.draw_coming_soon_screen("Options")

    def draw_high_scores(self):
        """Draw the high scores menu (placeholder)"""
        self.draw_coming_soon_screen("High Scores")

    def draw_coming_soon_screen(self, text: str):
        """Draw the placeholder coming soon screen"""
        # Simple "Coming soon" message and back button
        font = pygame.font.SysFont(None, 48)
        text = font.render(f"{text}: Coming Soon", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 250))
        self.screen.blit(text, text_rect)

        # Back button
        back_button = Button(WINDOW_WIDTH // 2 - 100, 400, 200, 50, "Back", self.button_color, self.button_hover)
        is_back_button_hovered = back_button.check_hover(pygame.mouse.get_pos())
        back_button.draw(self.screen, is_back_button_hovered)

        # TODO split up drawing and behaviour

        # Check for back button click
        if is_back_button_hovered and pygame.mouse.get_pressed()[0]:
            self.current_menu = MenuType.MAIN