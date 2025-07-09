import pygame
from pygame import Surface

from src.core.enum import PlayerColor
from src.util.config import GRID_SIZE

class TextureHunter:
    back: Surface | None = None
    front: Surface | None = None
    right: Surface | None = None
    left: Surface | None = None

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

    grass: Surface | None = None
    rock: Surface | None = None
    tree: Surface | None = None
    bush: Surface | None = None

    deer: Surface | None = None

    hunter: dict[PlayerColor, TextureHunter | None]

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

        cls.hunter[PlayerColor.GREEN].back = cls._load(cls.HUNTER_GREEN_BACK_PATH)
        cls.hunter[PlayerColor.GREEN].front = cls._load(cls.HUNTER_GREEN_FRONT_PATH)
        cls.hunter[PlayerColor.GREEN].left = cls._load(cls.HUNTER_GREEN_LEFT_PATH)
        cls.hunter[PlayerColor.GREEN].right = cls._load(cls.HUNTER_GREEN_RIGHT_PATH)

        cls.hunter[PlayerColor.RED].back = cls._load(cls.HUNTER_RED_BACK_PATH)
        cls.hunter[PlayerColor.RED].front = cls._load(cls.HUNTER_RED_FRONT_PATH)
        cls.hunter[PlayerColor.RED].left = cls._load(cls.HUNTER_RED_LEFT_PATH)
        cls.hunter[PlayerColor.RED].right = cls._load(cls.HUNTER_RED_RIGHT_PATH)

        cls.hunter[PlayerColor.BLUE].back = cls._load(cls.HUNTER_BLUE_BACK_PATH)
        cls.hunter[PlayerColor.BLUE].front = cls._load(cls.HUNTER_BLUE_FRONT_PATH)
        cls.hunter[PlayerColor.BLUE].left = cls._load(cls.HUNTER_BLUE_LEFT_PATH)
        cls.hunter[PlayerColor.BLUE].right = cls._load(cls.HUNTER_BLUE_RIGHT_PATH)

        cls.hunter[PlayerColor.YELLOW].back = cls._load(cls.HUNTER_YELLOW_BACK_PATH)
        cls.hunter[PlayerColor.YELLOW].front = cls._load(cls.HUNTER_YELLOW_FRONT_PATH)
        cls.hunter[PlayerColor.YELLOW].left = cls._load(cls.HUNTER_YELLOW_LEFT_PATH)
        cls.hunter[PlayerColor.YELLOW].right = cls._load(cls.HUNTER_YELLOW_RIGHT_PATH)
