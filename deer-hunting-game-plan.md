# Deer Picture Hunting Game: Development Plan

## 1. Python Implementation

### OOP Features for Game Structure
- **Class Hierarchy**: Create entity classes (GameObject → LivingEntity → Hunter/Deer)
- **Polymorphism**: Implement varying AI behaviors for different deer types
- **Encapsulation**: Use property decorators to control access to game state
- **Event System**: Design observer pattern for game events

### Key Libraries
- **Core**: Panda3D for 3D rendering and game logic
- **Math**: NumPy for efficient vector calculations
- **Networking**: Socket or Twisted for client-server communication
- **Concurrency**: Threading and asyncio for server operations

### Code Structure
```python
# Entity base classes
class GameObject:
    def __init__(self, position, model_path):
        self.position = position
        self.model = loader.loadModel(model_path)
        
    def update(self, dt):
        pass

class LivingEntity(GameObject):
    def __init__(self, position, model_path, speed, detection_radius):
        super().__init__(position, model_path)
        self.speed = speed
        self.detection_radius = detection_radius
        self.velocity = Vec3(0, 0, 0)
        
    def move(self, direction, dt):
        self.velocity = direction * self.speed
        new_pos = self.position + self.velocity * dt
        # Check collisions before moving
        if not self.would_collide(new_pos):
            self.position = new_pos
            self.model.setPos(self.position)
```

## 2. Panda3D Integration

### Setup and Initialization
```python
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *

class DeerHuntingGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        # Set up scene
        self.scene = self.loader.loadModel("models/environment")
        self.scene.reparentTo(self.render)
        
        # Set up lighting
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.2, 0.2, 0.2, 1))
        directional_light = DirectionalLight("directional_light")
        directional_light.setDirection((-1, -1, -1))
        directional_light.setColor((0.8, 0.8, 0.8, 1))
        
        # Set up collision system
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()
```

### Graphics and Scene Management
- Terrain generation using heightmaps
- Dynamic object loading and instancing for trees/rocks
- Level of detail system for performance
- Occlusion culling to improve rendering speed

### Physics and Collision
- Use Panda3D's built-in collision system
- Create collision geometry for all objects
- Implement ray-casting for line-of-sight checks
- Handle terrain collision for natural movement

## 3. Input System Implementation

### Player Controls
```python
def setup_controls(self):
    # Movement
    self.accept("w", self.start_move_forward)
    self.accept("w-up", self.stop_move_forward)
    self.accept("s", self.start_move_backward)
    self.accept("s-up", self.stop_move_backward)
    self.accept("a", self.start_turn_left)
    self.accept("a-up", self.stop_turn_left)
    self.accept("d", self.start_turn_right)
    self.accept("d-up", self.stop_turn_right)
    
    # Actions
    self.accept("mouse1", self.take_picture)
    self.accept("mouse3", self.zoom_camera)
    self.accept("mouse3-up", self.reset_zoom)
    
    # UI
    self.accept("escape", self.toggle_menu)
    
    # Mouse look
    self.disableMouse()
    self.taskMgr.add(self.mouse_look_task, "MouseLookTask")
```

### Camera System
- First-person view for immersive gameplay
- Zoom functionality for taking pictures
- Head bobbing for realistic movement
- Camera collision to prevent clipping

## 4. Game Mechanics

### World Design
- Large outdoor environment with varied terrain
- Dense forest areas with clearings
- Water features (streams, ponds)
- Natural paths and animal tracks
- Time of day system affecting visibility

### Deer AI System
```python
class DeerAI:
    def __init__(self, deer, world, difficulty_level):
        self.deer = deer
        self.world = world
        self.state = "CALM"  # States: CALM, ALERT, FLEEING
        self.detection_multiplier = self.get_difficulty_multiplier(difficulty_level)
        self.smell_radius = 20 * self.detection_multiplier
        self.sight_distance = 30 * self.detection_multiplier
        self.sight_angle = 120  # Degrees
        
    def update(self, dt):
        # Check for hunters
        hunters_detected = self.detect_hunters()
        
        if self.state == "CALM":
            if hunters_detected:
                self.state = "ALERT"
            else:
                self.wander(dt)
        
        elif self.state == "ALERT":
            if self.can_see_hunter():
                self.state = "FLEEING"
            else:
                self.move_away_from_smell(dt)
        
        elif self.state == "FLEEING":
            if not hunters_detected:
                self.fled_timer += dt
                if self.fled_timer > 10:  # Return to alert after 10 seconds
                    self.state = "ALERT"
            else:
                self.fled_timer = 0
                self.flee(dt)
    
    def detect_hunters(self):
        # Smell detection (circular)
        hunters_in_range = []
        for hunter in self.world.hunters:
            distance = (hunter.position - self.deer.position).length()
            if distance < self.smell_radius:
                hunters_in_range.append(hunter)
                
        # Sight detection (cone)
        for hunter in self.world.hunters:
            if self.can_see_entity(hunter):
                hunters_in_range.append(hunter)
                
        return hunters_in_range
```

### Photography System
- Ray-casting to detect what's in front of the camera
- Distance and angle calculations for scoring
- Photo storage with metadata
- Verification to check for other hunters in frame

### Scoring System
- Points for each unique deer
- Bonus points for rare deer types
- Extra points for close-up shots
- Penalty system for noise/movement
- Timer-based gameplay with configurable duration

## 5. Networking Architecture

### Client-Server Model
```python
# Server-side
class GameServer:
    def __init__(self, port=9999):
        self.port = port
        self.clients = {}
        self.world_state = WorldState()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(5)
        self.socket.setblocking(False)
        
    def start(self):
        asyncio.get_event_loop().run_until_complete(self.server_loop())
        
    async def server_loop(self):
        while True:
            # Accept new connections
            try:
                client_socket, address = await self.socket.accept()
                self.clients[address] = Client(client_socket, address)
                print(f"New client connected: {address}")
            except:
                pass
                
            # Process game updates
            self.update_world_state()
            
            # Send updates to clients
            await self.broadcast_world_state()
            
            # Process messages from clients
            for client in self.clients.values():
                await self.process_client_messages(client)
```

### State Synchronization
- Delta compression to reduce bandwidth
- Priority-based updates (nearby entities more frequent)
- Interpolation for smooth movement
- Prediction and reconciliation

### Lobby System
- Room creation and joining
- Player readiness states
- Game configuration options
- Chat functionality

## 6. Implementation Timeline

### Week 1: Core Setup (Complete)
- [✔] Project structure and version control
- [✔] Panda3D integration and basic rendering
- [✔] Player character and camera system
- [✔] Basic terrain and collision

### Week 2: Game Entities
- [ ] Deer models and basic movement
- [ ] Environment objects (trees, rocks)
- [ ] Basic AI for deer
- [ ] Player controls and movement

### Week 3: Game Mechanics
- [ ] Photography system implementation
- [ ] Advanced deer AI with smell/sight
- [ ] Scoring system
- [ ] UI elements and HUD

### Week 4: Networking
- [ ] Client-server architecture
- [ ] State synchronization
- [ ] Player representation in multiplayer
- [ ] Lobby system

### Week 5: Refinement
- [ ] Performance optimization
- [ ] Game balance
- [ ] Visual polish
- [ ] Bug fixing

### Week 6: Finalization
- [ ] Comprehensive testing
- [ ] Documentation
- [ ] Presentation preparation
- [ ] Final build and deployment

## 7. Testing Strategy

### Technical Testing
- Unit tests for critical systems
- Integration tests for subsystems
- Performance benchmarking
- Network stress testing

### Gameplay Testing
- Balance testing across difficulty levels
- User experience evaluation
- Multiplayer session testing
- Cross-platform verification

## 8. Preparation for Tasks 2 & 3

### Smalltalk Adaptation (Task 2)
- Study Squeak environment
- Identify reusable components
- Plan UI simplifications
- Research Smalltalk design patterns

### Eiffel Adaptation (Task 3)
- Study EiffelStudio
- Plan contract-based design
- Design assertions and invariants
- Prepare terminal-based fallback UI
