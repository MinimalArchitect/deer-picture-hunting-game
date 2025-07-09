class GameConfig:
    MIN_LEVEL = 1
    MAX_LEVEL = 20

    TILE_SIZE = 30  # in pixel
    GRID_WIDTH, GRID_HEIGHT = 40, 30
    WINDOW_WIDTH, WINDOW_HEIGHT = (GRID_WIDTH * TILE_SIZE, GRID_HEIGHT * TILE_SIZE)

    FRAME_RATE = 10

    DEER_COUNT = 10
    PHOTO_RANGE = 10

    GAME_DURATION = 60  # in seconds


class GameServerConfig(GameConfig):
    def __init__(self) -> None:
        self._host: tuple[str, int] = ("0.0.0.0", 12345)

    @property
    def host(self) -> tuple[str, int]:
        return self._host


class GameClientConfig(GameConfig):
    SCORE_FILE = 'level_scores.json'

    def __init__(self):
        pass
