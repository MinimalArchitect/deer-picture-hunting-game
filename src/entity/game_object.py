class GameObject:
    """Base class for all game objects"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, surface):
        pass

    def update(self):
        pass