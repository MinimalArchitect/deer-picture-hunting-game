class GameObject:
    """Base class for all game objects"""

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def draw(self, surface):
        pass

    def update(self):
        pass