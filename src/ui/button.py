import pygame

from src.util.color import Color


class Button:
    """Interactive button for menu screens"""

    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.font = pygame.font.SysFont(None, 32)

    def draw(self, surface, is_hovered=None):
        # Handle case where is_hovered is not provided
        if is_hovered is None:
            is_hovered = self.check_hover(pygame.mouse.get_pos())
            
        # Draw button with appropriate color based on hover state
        color = self.hover_color if is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, Color.BLACK, self.rect, 2)  # Border

        # Draw text
        text_surface = self.font.render(self.text, True, Color.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over button"""
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos, mouse_click):
        """Check if button is clicked"""
        return self.rect.collidepoint(mouse_pos) and mouse_click