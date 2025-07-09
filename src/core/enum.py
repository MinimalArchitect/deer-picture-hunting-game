from enum import StrEnum, Enum


class MoveDirection(StrEnum):
    """GameObject direction"""
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Tile(StrEnum):
    """Types of grid tiles"""
    EMPTY = "."
    TREE = "T"
    ROCK = "R"
    BUSH = "B"
    DEER = "D"
    PLAYER = "P"

class PlayerColor(Enum):
    """Player color"""
    RED = "RED"
    GREEN = "GREEN"
    BLUE = "BLUE"
    YELLOW = "YELLOW"