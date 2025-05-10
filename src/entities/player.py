"""
Player class that handles movement and actions
"""
from direct.showbase.ShowBaseGlobal import globalClock
from direct.task import Task
from panda3d.core import Vec3, CollisionSphere, CollisionNode

from src.entities.game_object import GameObject
from src.core.camera_controller import CameraController


class Player(GameObject):
    """Player character that the user controls"""

    def __init__(self, base, start_pos=None):
        """
        Initialize the player
        
        Args:
            base: The ShowBase instance
            start_pos (Vec3, optional): Starting position
        """
        super().__init__(base=base, position=start_pos or Vec3(0, 0, 0))

        self.base = base
        self.speed = 5.0  # Movement speed in units per second

        # Movement flags
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False

        # Create a collision sphere
        self.setup_collision()

        # Set up camera
        self.camera_controller = CameraController(base)

        # Register tasks
        self.base.taskMgr.add(self.move_task, "PlayerMoveTask")

        # Set up input handling
        self.setup_controls()

    def setup_collision(self):
        """Set up collision detection for the player"""
        # Create collision sphere
        collision_sphere = CollisionSphere(0, 0, 0, 0.5)  # 0.5 unit radius
        collision_node = CollisionNode("player")
        collision_node.addSolid(collision_sphere)

        # Attach collision node to player
        self.collision_np = self.base.render.attachNewNode(collision_node)
        self.collision_np.setPos(self.position)

        # Add to traverser and handler
        self.base.cTrav.addCollider(self.collision_np, self.base.pusher)
        self.base.pusher.addCollider(self.collision_np, self.collision_np)

    def setup_controls(self):
        """Set up keyboard and mouse controls"""
        # Movement controls
        self.base.accept("w", self.set_moving, [True, False, False, False])
        self.base.accept("w-up", self.set_moving, [False, False, False, False])

        self.base.accept("s", self.set_moving, [False, True, False, False])
        self.base.accept("s-up", self.set_moving, [False, False, False, False])

        self.base.accept("a", self.set_moving, [False, False, True, False])
        self.base.accept("a-up", self.set_moving, [False, False, False, False])

        self.base.accept("d", self.set_moving, [False, False, False, True])
        self.base.accept("d-up", self.set_moving, [False, False, False, False])

        # Camera controls
        self.base.accept("mouse1", self.take_picture)
        self.base.accept("mouse3", self.zoom_in)
        self.base.accept("mouse3-up", self.zoom_out)

    def set_moving(self, forward, backward, left, right):
        """Set movement flags based on key presses"""
        self.moving_forward = forward
        self.moving_backward = backward
        self.moving_left = left
        self.moving_right = right

    def move_task(self, task):
        """Update player position based on movement flags"""
        # Calculate time since last update
        dt = globalClock.getDt()

        # Get camera direction vectors
        forward_vec = self.base.camera.getQuat().getForward()
        right_vec = self.base.camera.getQuat().getRight()

        # Remove vertical component
        forward_vec.setZ(0)
        forward_vec.normalize()
        right_vec.setZ(0)
        right_vec.normalize()

        # Calculate movement direction
        move_direction = Vec3(0, 0, 0)

        if self.moving_forward:
            move_direction += forward_vec
        if self.moving_backward:
            move_direction -= forward_vec
        if self.moving_right:
            move_direction += right_vec
        if self.moving_left:
            move_direction -= right_vec

        # Normalize if non-zero
        if move_direction.length() > 0:
            move_direction.normalize()

        # Calculate new position
        move_amount = move_direction * self.speed * dt
        new_pos = self.position + move_amount

        # Update position
        self.position = new_pos
        self.collision_np.setPos(self.position)

        # Update camera position (keep height constant)
        self.base.camera.setPos(
            self.position.getX(),
            self.position.getY(),
            self.position.getZ() + self.camera_controller.height
        )

        return Task.cont

    def take_picture(self):
        """Take a picture of what's in front of the camera"""
        print("Taking picture!")
        # This will be implemented in Week 3

    def zoom_in(self):
        """Zoom in the camera"""
        self.camera_controller.zoom(True)

    def zoom_out(self):
        """Zoom out the camera"""
        self.camera_controller.zoom(False)
