import pygame
from pygame.font import Font


class GameFont:
    heading1_font: Font = None
    text_font: Font = None
    version_font: Font = None
    button_text_font: Font = None

    @classmethod
    def load_all(cls):
        cls.heading1_font = pygame.font.SysFont(None, 64)
        cls.text_font = pygame.font.SysFont(None, 36)
        cls.button_text_font = pygame.font.SysFont(None, 32)
        cls.version_font = pygame.font.SysFont(None, 24)