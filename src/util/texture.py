import pygame

from src.util.config import GRID_SIZE


class Texture:
    GRASS_PATH = "assets/textures/grass.png"
    ROCK_PATH = "assets/textures/rock.png"
    TREE_PATH = "assets/textures/tree.png"
    BUSH_PATH = "assets/textures/bush.png"
    DEER_PATH = "assets/textures/deer.png"
    HUNTER_BACK_PATH = "assets/textures/hunter-back.png"
    HUNTER_FRONT_PATH = "assets/textures/hunter-front.png"
    HUNTER_LEFT_PATH = "assets/textures/hunter-left.png"
    HUNTER_RIGHT_PATH = "assets/textures/hunter-right.png"

    grass = None
    rock = None
    tree = None
    bush = None
    deer = None

    hunter_back = None
    hunter_front = None
    hunter_right = None
    hunter_left = None

    @classmethod
    def _load(cls, path: str):
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, (GRID_SIZE, GRID_SIZE))

    @classmethod
    def load_all(cls):
        Texture.grass = Texture._load(Texture.GRASS_PATH)
        Texture.rock = Texture._load(Texture.ROCK_PATH)
        Texture.tree = Texture._load(Texture.TREE_PATH)
        Texture.bush = Texture._load(Texture.BUSH_PATH)

        Texture.deer = Texture._load(Texture.DEER_PATH)

        Texture.hunter_back = Texture._load(Texture.HUNTER_BACK_PATH)
        Texture.hunter_front = Texture._load(Texture.HUNTER_FRONT_PATH)
        Texture.hunter_right = Texture._load(Texture.HUNTER_RIGHT_PATH)
        Texture.hunter_left = Texture._load(Texture.HUNTER_LEFT_PATH)
