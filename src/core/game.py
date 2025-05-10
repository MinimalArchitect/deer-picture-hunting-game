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


class DeerHuntingGame(ShowBase):
    """Main game class for the Deer Picture Hunting Game"""

    def __init__(self):
        """Initialize the game"""
        ShowBase.__init__(self)

        # Set window properties
        self.set_window_properties()

        # Set up collision system
        self.setup_collision()

        # Set up lighting
        self.setup_lighting()

        getModelPath().appendDirectory(Filename.fromOsSpecific("assets"))

        # Create terrain
        self.terrain = Terrain(self)

        # Create player
        self.player = Player(self, Vec3(0, 0, 3))

        # Create deer
        self.deer_list = []
        self.spawn_deer()

        self.setBackgroundColor(0.6, 0.8, 1.0)  # Light blue sky

        self.render.setShaderAuto()  # Enable automatic shaders

        # Display instructions
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

    def spawn_deer(self):
        """Spawn deer entities at fixed positions"""
        positions = [Vec3(10, 10, 0), Vec3(-15, 25, 0), Vec3(20, -20, 0)]
        for pos in positions:
            deer = Deer(self, pos)
            self.deer_list.append(deer)

    def setup_skybox(self):
        """Create a simple skybox"""
        # Load a sky sphere model
        self.sky = self.loader.loadModel("models/sky_sphere")
        self.sky.setScale(10000)  # Make it big enough to encompass the scene

        # Use a simple blue texture for the sky
        sky_tex = self.loader.loadTexture("assets/textures/sky.jpg")
        self.sky.setTexture(sky_tex, 1)

        # Attach it to the camera so it moves with the view
        self.sky.reparentTo(self.render)
        self.sky.setBin("background", 0)
        self.sky.setDepthWrite(False)

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

        self.instruction_text = OnscreenText(
            text="\n".join(instructions),
            pos=(-0.95, 0.8),
            scale=0.07,
            fg=(1, 1, 1, 1),
            align=TextNode.ALeft,
            mayChange=False
        )
