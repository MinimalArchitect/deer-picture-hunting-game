"""
Terrain generation and collision
"""
from panda3d.core import TextureStage, GeoMipTerrain, Vec3, Vec4, CollisionNode, CollisionPlane, Plane, BitMask32

class Terrain:
    """Generates and manages the game terrain"""

    def __init__(self, base, heightmap_path="assets/textures/heightmap.png"):
        """
        Initialize the terrain
        
        Args:
            base: The ShowBase instance
            heightmap_path (str): Path to the heightmap image
        """
        self.base = base

        # Create GeoMipTerrain
        self.terrain = GeoMipTerrain("terrain")
        self.terrain.setHeightfield(heightmap_path)

        # Set terrain scale
        self.terrain.setBlockSize(64)
        self.terrain.setNear(40)
        self.terrain.setFar(100)
        self.terrain.setFocalPoint(self.base.camera)

        # Set terrain properties
        terrain_node = self.terrain.getRoot()
        self.root_node = terrain_node
        terrain_node.setSz(10)  # Height scale
        terrain_node.setPos(-50, 0, -2)  # Position

        # Generate
        self.terrain.generate()

        # Apply textures
        self.apply_textures()

        # Add terrain to scene
        terrain_node.reparentTo(self.base.render)

        # Set up collision
        self.setup_collision()

        # Add terrain update task
        self.base.taskMgr.add(self.update, "TerrainUpdateTask")

    def apply_textures(self):
        """Apply textures to the terrain"""
        # Get terrain node
        terrain_node = self.terrain.getRoot()

        # Load grass texture
        grass_tex = self.base.loader.loadTexture("assets/textures/grass.jpg")
        if grass_tex:
            # Set texture properties
            grass_tex.setWrapU(grass_tex.WM_repeat)
            grass_tex.setWrapV(grass_tex.WM_repeat)

            # Apply texture
            ts = TextureStage.getDefault()
            terrain_node.setTexture(ts, grass_tex)
            terrain_node.setTexScale(ts, 100, 100)

            print("Texture applied successfully!")
        else:
            print("Failed to load texture!")

    def setup_collision(self):
        """Set up collision for the terrain"""
        # For now, just create a simple ground plane
        # Later, we'll use the actual terrain height for collision
        # plane = Plane(Vec3(0, 0, 1), Vec3(0, 0, 0))
        # collision_node = CollisionNode("terrain_collision")
        # collision_node.addSolid(CollisionPlane(plane))
        # collision_np = self.base.render.attachNewNode(collision_node)

        """Set up collision for the terrain using terrain root node"""
        root = self.terrain.getRoot()
        root.reparentTo(self.base.render)
        root.setCollideMask(BitMask32.bit(1))  # Enable collision

    def get_elevation(self, x, y):
        """Return terrain height at given (x, y) position"""
        return self.terrain.getElevation(x + 50, y) * 10 - 2  # Offset terrain origin

    def update(self, task):
        """Update the terrain (for LOD)"""
        self.terrain.update()
        return task.cont