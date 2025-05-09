"""
Base class for all game objects
"""
from panda3d.core import Vec3, NodePath

class GameObject:
    """Base class for all objects in the game"""
    
    def __init__(self, position=None, model_path=None):
        """
        Initialize a game object
        
        Args:
            position (Vec3, optional): Initial position of the object
            model_path (str, optional): Path to the model file
        """
        self.position = position or Vec3(0, 0, 0)
        self.node_path = None
        
        if model_path:
            self.load_model(model_path)
            
    def load_model(self, model_path):
        """
        Load a 3D model for this object
        
        Args:
            model_path (str): Path to the model file
        """
        # Note: This requires access to the loader from ShowBase
        # We'll need to pass this from the game instance in practice
        base = self.get_base()
        self.node_path = base.loader.loadModel(model_path)
        self.node_path.setPos(self.position)
        self.node_path.reparentTo(base.render)
        
    def get_base(self):
        """
        Get the ShowBase instance
        This is a placeholder for now - we'll improve it later
        """
        from direct.showbase.ShowBase import ShowBase
        return ShowBase.instance
        
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