from direct.showbase import ShowBase


class GameState:
    def __init__(self, base: ShowBase):
        self.base = base
        self.is_paused = False