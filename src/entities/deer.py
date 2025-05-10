from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec3
from src.entities.game_object import GameObject
from random import uniform
from direct.task import Task


class Deer(GameObject):
    """Basic deer entity with idle movement"""

    def __init__(self, base, start_position):
        super().__init__(base=base, position=start_position, model_path="models/ball.egg")
        self.base = base
        self.speed = 1.0  # Units per second
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
        return Task.cont
