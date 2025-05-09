"""
Camera controller for first-person perspective
"""
from direct.task import Task
from panda3d.core import Vec3

class CameraController:
    """Handles camera positioning and movement for first-person view"""
    
    def __init__(self, base):
        """
        Initialize the camera controller
        
        Args:
            base: The ShowBase instance
        """
        self.base = base
        self.camera = base.camera
        
        # Camera settings
        self.height = 1.75  # Eye height in meters
        self.pitch_limit = 90  # Vertical look limit in degrees
        self.mouse_sensitivity = 0.15
        self.zoom_fov = 20  # Field of view when zoomed
        self.normal_fov = 70  # Normal field of view
        self.is_zoomed = False
        
        # Disable default mouse control
        self.base.disableMouse()
        
        # Set initial position
        self.camera.setPos(0, 0, self.height)
        
        # Set up tasks
        self.base.taskMgr.add(self.camera_task, "CameraTask")
        
        # Track mouse position
        self.last_mouse_x = 0
        self.last_mouse_y = 0
        self.heading = 0
        self.pitch = 0
        
        # Set initial FOV
        self.base.camLens.setFov(self.normal_fov)
        
    def camera_task(self, task):
        """Update camera position and orientation"""
        # Only update if mouse is available
        if self.base.mouseWatcherNode.hasMouse():
            # Get mouse position
            mouse_pos = self.base.mouseWatcherNode.getMouse()
            
            # Calculate mouse movement
            dx = mouse_pos.getX() - self.last_mouse_x
            dy = mouse_pos.getY() - self.last_mouse_y
            
            # Update camera orientation
            self.heading -= dx * self.mouse_sensitivity * 100
            self.pitch += dy * self.mouse_sensitivity * 100
            
            # Clamp pitch to limits
            self.pitch = max(-self.pitch_limit, min(self.pitch_limit, self.pitch))
            
            # Set camera orientation
            self.camera.setHpr(self.heading, self.pitch, 0)
            
            # Store current mouse position
            self.last_mouse_x = mouse_pos.getX()
            self.last_mouse_y = mouse_pos.getY()
        
        return Task.cont
        
    def zoom(self, zoom_in=True):
        """Zoom the camera in or out"""
        if zoom_in and not self.is_zoomed:
            self.base.camLens.setFov(self.zoom_fov)
            self.is_zoomed = True
        elif not zoom_in and self.is_zoomed:
            self.base.camLens.setFov(self.normal_fov)
            self.is_zoomed = False