import pygame


class Sound:
    MOVE_PATH = "assets/sounds/carton_move.wav"
    PHOTO_PATH = "assets/sounds/camera-photo-snap.wav"

    move = None
    take_photo = None

    @classmethod
    def _load(cls, path: str):
        return pygame.mixer.Sound(path)

    @classmethod
    def load_all(cls):
        cls.move = cls._load(cls.MOVE_PATH)
        cls.take_photo = cls._load(cls.PHOTO_PATH)
