import pygame

from src.util.config import GRID_SIZE


class Texture:
    GRASS_PATH = "assets/textures/grass.png"
    ROCK_PATH = "assets/textures/rock.png"
    TREE_PATH = "assets/textures/tree.png"
    BUSH_PATH = "assets/textures/bush.png"

    DEER_PATH = "assets/textures/deer.png"

    HUNTER_GREEN_BACK_PATH = "assets/textures/hunter-green-back.png"
    HUNTER_GREEN_FRONT_PATH = "assets/textures/hunter-green-front.png"
    HUNTER_GREEN_LEFT_PATH = "assets/textures/hunter-green-left.png"
    HUNTER_GREEN_RIGHT_PATH = "assets/textures/hunter-green-right.png"

    HUNTER_BLUE_BACK_PATH = "assets/textures/hunter-blue-back.png"
    HUNTER_BLUE_FRONT_PATH = "assets/textures/hunter-blue-front.png"
    HUNTER_BLUE_LEFT_PATH = "assets/textures/hunter-blue-left.png"
    HUNTER_BLUE_RIGHT_PATH = "assets/textures/hunter-blue-right.png"

    HUNTER_RED_BACK_PATH = "assets/textures/hunter-red-back.png"
    HUNTER_RED_FRONT_PATH = "assets/textures/hunter-red-front.png"
    HUNTER_RED_LEFT_PATH = "assets/textures/hunter-red-left.png"
    HUNTER_RED_RIGHT_PATH = "assets/textures/hunter-red-right.png"

    HUNTER_YELLOW_BACK_PATH = "assets/textures/hunter-yellow-back.png"
    HUNTER_YELLOW_FRONT_PATH = "assets/textures/hunter-yellow-front.png"
    HUNTER_YELLOW_LEFT_PATH = "assets/textures/hunter-yellow-left.png"
    HUNTER_YELLOW_RIGHT_PATH = "assets/textures/hunter-yellow-right.png"

    grass = None
    rock = None
    tree = None
    bush = None

    deer = None

    hunter_green_back = None
    hunter_green_front = None
    hunter_green_right = None
    hunter_green_left = None

    hunter_blue_back = None
    hunter_blue_front = None
    hunter_blue_right = None
    hunter_blue_left = None

    hunter_red_back = None
    hunter_red_front = None
    hunter_red_right = None
    hunter_red_left = None

    hunter_yellow_back = None
    hunter_yellow_front = None
    hunter_yellow_right = None
    hunter_yellow_left = None

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

        cls.hunter_green_back = cls._load(cls.HUNTER_GREEN_BACK_PATH)
        cls.hunter_green_front = cls._load(cls.HUNTER_GREEN_FRONT_PATH)
        cls.hunter_green_right = cls._load(cls.HUNTER_GREEN_RIGHT_PATH)
        cls.hunter_green_left = cls._load(cls.HUNTER_GREEN_LEFT_PATH)

        cls.hunter_blue_back = cls._load(cls.HUNTER_BLUE_BACK_PATH)
        cls.hunter_blue_front = cls._load(cls.HUNTER_BLUE_FRONT_PATH)
        cls.hunter_blue_right = cls._load(cls.HUNTER_BLUE_RIGHT_PATH)
        cls.hunter_blue_left = cls._load(cls.HUNTER_BLUE_LEFT_PATH)

        cls.hunter_red_back = cls._load(cls.HUNTER_RED_BACK_PATH)
        cls.hunter_red_front = cls._load(cls.HUNTER_RED_FRONT_PATH)
        cls.hunter_red_right = cls._load(cls.HUNTER_RED_RIGHT_PATH)
        cls.hunter_red_left = cls._load(cls.HUNTER_RED_LEFT_PATH)

        cls.hunter_yellow_back = cls._load(cls.HUNTER_YELLOW_BACK_PATH)
        cls.hunter_yellow_front = cls._load(cls.HUNTER_YELLOW_FRONT_PATH)
        cls.hunter_yellow_right = cls._load(cls.HUNTER_YELLOW_RIGHT_PATH)
        cls.hunter_yellow_left = cls._load(cls.HUNTER_YELLOW_LEFT_PATH)
