import json
import os

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

        self.level_scores = {}

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
        # Load scores from file
        score_file = "level_scores.json"
        self.level_scores = {}
        if os.path.exists(score_file):
            try:
                with open(score_file, "r") as f:
                    self.level_scores = json.load(f)
            except Exception as e:
                print("Error loading scores:", e)

        # Draw background
        self.screen.fill(Color.BACKGROUND)

        # Draw title
        font = pygame.font.SysFont(None, 64)
        title_text = font.render("High Scores", True, Color.BLACK)
        self.screen.blit(title_text, (WINDOW_WIDTH // 2 - 130, 60))

        # Draw scores in two columns
        score_font = pygame.font.SysFont(None, 32)
        column_x = [WINDOW_WIDTH // 2 - 180, WINDOW_WIDTH // 2 + 20]
        y_start = 140
        line_spacing = 30

        for i, level in enumerate(range(1, 21)):
            col = 0 if level <= 10 else 1
            row = i if level <= 10 else i - 10
            y = y_start + row * line_spacing
            key = str(level)
            score = self.level_scores.get(key, None)
            text = f"Level {level}: {score if score is not None else '-'}"
            line = score_font.render(text, True, Color.BLACK)
            self.screen.blit(line, (column_x[col], y))

        # Back and Reset buttons
        back_btn = Button(WINDOW_WIDTH // 2 - 140, 500, 120, 40, "Back", Color.BUTTON, Color.BUTTON_HOVER)
        reset_btn = Button(WINDOW_WIDTH // 2 + 20, 500, 120, 40, "Reset", Color.BUTTON, Color.BUTTON_HOVER)

        back_btn.draw(self.screen, back_btn.check_hover(pygame.mouse.get_pos()))
        reset_btn.draw(self.screen, reset_btn.check_hover(pygame.mouse.get_pos()))

        pygame.display.flip()

        # Handle button clicks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_btn.is_clicked(mouse_pos, True):
                    self.current_menu = MenuType.MAIN
                elif reset_btn.is_clicked(mouse_pos, True):
                    self.level_scores = {}
                    if os.path.exists(score_file):
                        try:
                            os.remove(score_file)
                        except Exception as e:
                            print("Error resetting score file:", e)

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
