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
        cls.grass = cls._load(cls.GRASS_PATH)
        cls.rock = cls._load(cls.ROCK_PATH)
        cls.tree = cls._load(cls.TREE_PATH)
        cls.bush = cls._load(cls.BUSH_PATH)

        cls.deer = cls._load(cls.DEER_PATH)

        cls.hunter_back = cls._load(cls.HUNTER_BACK_PATH)
        cls.hunter_front = cls._load(cls.HUNTER_FRONT_PATH)
        cls.hunter_right = cls._load(cls.HUNTER_RIGHT_PATH)
        cls.hunter_left = cls._load(cls.HUNTER_LEFT_PATH)
