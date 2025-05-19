import pygame

from src.util.config import GRID_SIZE


class Texture:
    GRASS_PATH = "assets/textures/grass.png"
    ROCK_PATH = "assets/textures/rock.png"
    TREE_PATH = "assets/textures/tree.png"
    BUSH_PATH = "assets/textures/bush.png"

    DEER_PATH = "assets/textures/deer.png"

    GREEN_HUNTER_BACK_PATH = "assets/textures/green-hunter-back.png"
    GREEN_HUNTER_FRONT_PATH = "assets/textures/green-hunter-front.png"
    GREEN_HUNTER_LEFT_PATH = "assets/textures/green-hunter-left.png"
    GREEN_HUNTER_RIGHT_PATH = "assets/textures/green-hunter-right.png"

    grass = None
    rock = None
    tree = None
    bush = None

    deer = None

    green_hunter_back = None
    green_hunter_front = None
    green_hunter_right = None
    green_hunter_left = None

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

        cls.green_hunter_back = cls._load(cls.GREEN_HUNTER_BACK_PATH)
        cls.green_hunter_front = cls._load(cls.GREEN_HUNTER_FRONT_PATH)
        cls.green_hunter_right = cls._load(cls.GREEN_HUNTER_RIGHT_PATH)
        cls.green_hunter_left = cls._load(cls.GREEN_HUNTER_LEFT_PATH)
