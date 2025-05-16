from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec3, CollisionSphere, CollisionNode, BitMask32
from src.entities.game_object import GameObject
from random import uniform
from direct.task import Task


class Deer(GameObject):
    """Basic deer entity with idle movement"""

    def __init__(self, base, start_position):
        super().__init__(base=base, position=start_position, model_path="models/ball.egg")
        self.base = base
        self.speed = 1.0  # Units per second
        self.setup_collision()
        self.direction = Vec3(uniform(-1, 1), uniform(-1, 1), 0)
        self.direction.normalize()

        # Set up idle movement task
        self.base.taskMgr.add(self.idle_move_task, "DeerIdleMove")

    def idle_move_task(self, task):
        """Make the deer wander slowly"""
        dt = globalClock.getDt()
        move = self.direction * self.speed * dt
        self.position += move
        if self.node_path:
            self.node_path.setPos(self.position)
        if self.collision_np:
            self.collision_np.setPos(self.position)
        self.apply_gravity(dt)
        if self.collision_np:
            self.collision_np.setPos(self.position)
        return Task.cont

    def setup_collision(self):
        """Set up collision detection for the deer"""
        collision_sphere = CollisionSphere(0, 0, 0, 0.5)
        collision_node = CollisionNode("deer")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(BitMask32.bit(1))
        collision_node.setIntoCollideMask(BitMask32.bit(1))

        self.collision_np = self.base.render.attachNewNode(collision_node)
        self.collision_np.setPos(self.position)

        self.base.cTrav.addCollider(self.collision_np, self.base.pusher)
        self.base.pusher.addCollider(self.collision_np, self.collision_np)
