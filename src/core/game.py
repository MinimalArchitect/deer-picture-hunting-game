import pygame

from src.core.game_context import GameContext
from src.core.state_machine import StateMachine
from src.ui.gamefont import GameFont
from src.util.config import WINDOW_WIDTH, WINDOW_HEIGHT
from src.util.sound import Sound
from src.util.texture import Texture


# TODO: multiple deer difficulties
# TODO: multiplayer game state
# TODO: multiplayer game server
# TODO: overhaul finished game state
# TODO: introduce server selection
# TODO: introduce player color selection
class Game:
    """Main game class"""

    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Deer Picture Hunting")

        # Load textures and sounds
        Texture.load_all()
        Sound.load_all()
        GameFont.load_all()

        self.state_machine = StateMachine(
            GameContext(
                screen,
                pygame.time.Clock()
            )
        )

    def run(self):
        while self.state_machine.is_running():
            self.state_machine.update()

        self.state_machine.shutdown()
