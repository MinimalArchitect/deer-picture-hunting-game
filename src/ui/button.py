import pygame

from src.ui.gamefont import GameFont
from src.util.color import Color

class DefaultButtonConfig:
    default_height = 50
    default_width = 200

class Button:
    def __init__(self, text, x, y, width=DefaultButtonConfig.default_width, height=DefaultButtonConfig.default_height, color=Color.BUTTON, hover_color=Color.BUTTON_HOVER):
        self.width, self.height = width, height
        self.x, self.y = x, y
        self.rect = pygame.Rect(x, y, width, height)

        self.font = GameFont.button_text_font
        self.color = color
        self.hover_color = hover_color
        self.disabled_color = Color.GRAY

        self.text = text

        self.is_hovered = False
        self.is_disabled = False


    def draw(self, surface, is_hovered=None):
        # Handle case where is_hovered is not provided
        if is_hovered is None:
            is_hovered = self.check_hover(pygame.mouse.get_pos())
            
        # Draw button with appropriate color based on hover state
        color = self.hover_color if is_hovered else self.color
        color = self.disabled_color if self.is_disabled else color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)  # Border

        # Draw text
        text_surface = self.font.render(self.text, True, Color.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over button"""
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos)

    def width(self) -> int:
        return self.width

    def height(self) -> int:
        return self.height

    def disable(self):
        self.is_disabled = True

    def enable(self):
        self.is_disabled = False