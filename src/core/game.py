"""
Main game class that initializes and runs the game
"""
from direct.showbase.ShowBase import ShowBase
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import WindowProperties, AmbientLight, DirectionalLight, getModelPath, Filename
from panda3d.core import Vec3, Vec4, CollisionTraverser, CollisionHandlerPusher, TextNode

from src.entities.player import Player
from src.physics.terrain import Terrain
from src.entities.deer import Deer

USE_PANDA_ENVIRONMENT = True


class DeerHuntingGame(ShowBase):
    """Main game class for the Deer Picture Hunting Game"""

    def __init__(self):
        ShowBase.__init__(self)

        self.set_window_properties()

        self.setup_collision()

        self.setup_lighting()

        getModelPath().appendDirectory(Filename.fromOsSpecific("assets"))

        if USE_PANDA_ENVIRONMENT:
            self.load_environment()
        else:
            self.terrain = Terrain(self)

        self.player = Player(self, Vec3(0, 0, 3))

        self.deer_list = []
        self.spawn_deer()

        self.setBackgroundColor(0.6, 0.8, 1.0)  # Light blue sky
        self.render.setShaderAuto()  # Enable automatic shaders

        self.display_instructions()

    def set_window_properties(self):
        """Set up the game window properties"""
        props = WindowProperties()
        props.setTitle("Deer Picture Hunting Game")
        props.setSize(1024, 768)
        self.win.requestProperties(props)

    def setup_lighting(self):
        """Set up basic lighting in the scene"""
        # Ambient light
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor(Vec4(0.4, 0.4, 0.4, 1))  # Brighter ambient light
        ambient_light_np = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_light_np)

        # Directional light (sun)
        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(Vec4(0.9, 0.9, 0.8, 1))  # Brighter directional light
        directional_light.setDirection(Vec3(-1, -1, -0.5))
        directional_light_np = self.render.attachNewNode(directional_light)
        self.render.setLight(directional_light_np)

    def setup_collision(self):
        """Set up the collision system"""
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

    def load_environment(self):
        """Load trees and rocks environment model"""
        environment = self.loader.loadModel("models/environment.egg")
        environment.reparentTo(self.render)
        environment.setScale(0.25, 0.25, 0.25)
        environment.setPos(-8, 42, 0)

    def spawn_deer(self):
        """Spawn deer entities at fixed positions"""
        positions = [Vec3(10, 10, 0), Vec3(-15, 25, 0), Vec3(20, -20, 0)]
        for pos in positions:
            deer = Deer(self, pos)
            self.deer_list.append(deer)

    def display_instructions(self):
        """Display game instructions on the screen"""
        instructions = [
            "Deer Picture Hunting Game - Development Build",
            "W/A/S/D: Move",
            "Mouse: Look around",
            "Left Click: Take picture",
            "Right Click: Zoom",
            "ESC: Pause/Menu"
        ]

        OnscreenText(
            text="\n".join(instructions),
            pos=(-0.95, 0.8),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=False
        )
