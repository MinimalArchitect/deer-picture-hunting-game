from panda3d.core import Vec3


class GameObject:
    """Base class for all objects in the game"""

    def __init__(self, base, position=None, model_path=None):
        self.base = base  # Save reference to ShowBase
        self.position = position or Vec3(0, 0, 0)
        self.node_path = None

        if model_path:
            self.load_model(model_path)

    def load_model(self, model_path):
        print(f"[Info] Loading model: {model_path}")
        self.node_path = self.base.loader.loadModel(model_path)
        self.node_path.setPos(self.position)
        self.node_path.reparentTo(self.base.render)

    def update(self, dt):
        """
        Update the object state
        
        Args:
            dt (float): Time delta since last update
        """
        pass

    def remove(self):
        """Remove the object from the scene"""
        if self.node_path and not self.node_path.isEmpty():
            self.node_path.removeNode()
