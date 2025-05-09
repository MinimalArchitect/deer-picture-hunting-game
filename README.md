# Deer Picture Hunting Game

A 3D game where players hunt for deer photographs in a forest environment. This game is being developed as part of the Advanced Object-Oriented Programming course at TU Wien.

![Game Screenshot](https://github.com/MinimalArchitect/deer-picture-hunting-game/raw/main/screenshots/week1.png)

## Current game plan:

- [Game Plan](deer-hunting-game-plan.md)

## Project Overview

Deer Picture Hunting Game is a 3D first-person photography game where players take pictures of deer in a forest environment. The game will feature:

- First-person camera controls
- Realistic deer AI with smell and sight detection
- Various terrain and environments
- Scoring system for photographs
- Multiplayer capabilities in the final version

This project is being developed in three phases, each using a different programming language:
1. Python with Panda3D (Current phase)
2. Smalltalk implementation
3. Eiffel implementation

## Implementation Status

**Current Version: Week 1 - Core Setup**

We have implemented the core game engine with:
- 3D terrain rendering
- First-person camera controls
- Basic movement mechanics
- Collision detection
- Photography mechanic (basic implementation)
- Development environment configuration

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Panda3D 1.10.x

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/MinimalArchitect/deer-picture-hunting-game.git
   cd deer-picture-hunting-game
   ```

2. Create and activate a virtual environment:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install panda3d
   pip install numpy  # For future physics calculations
   ```

4. Ensure you have the required assets:
   - Create `assets/textures` directory if it doesn't exist
   - Add a seamless grass texture named `grass.jpg`
   - Add a heightmap image named `heightmap.png` (257x257 pixels recommended)

## Running the Game

To start the game in development mode:

```bash
# From the project root
python tests/test_game.py

# Or alternatively
python src/main.py
```

### Controls

- **W, A, S, D**: Move forward, left, backward, right
- **Mouse**: Look around
- **Left-click**: Take picture
- **Right-click (hold)**: Zoom in
- **ESC**: Pause/Menu (not implemented yet)

## Project Structure

```
deer-picture-hunting-game/
├── src/                    # Source code
│   ├── core/               # Core game systems
│   │   ├── game.py         # Main game class
│   │   └── camera_controller.py  # Camera handling
│   ├── entities/           # Game entities
│   │   ├── game_object.py  # Base object class
│   │   └── player.py       # Player implementation
│   ├── physics/            # Physics systems
│   │   └── terrain.py      # Terrain generation
│   ├── ui/                 # User interface (future)
│   └── networking/         # Networking code (future)
├── assets/                 # Game assets
│   ├── models/             # 3D models
│   ├── textures/           # Texture files
│   └── sounds/             # Sound effects (future)
├── tests/                  # Test scripts
│   └── test_game.py        # Basic game testing
└── docs/                   # Documentation (future)
```

## Features

### Implemented (Week 1)

- **Core Engine Setup**: Based on Panda3D with Python
- **Terrain System**: Heightmap-based terrain with texture mapping
- **Camera Controls**: First-person view with mouse look
- **Movement System**: WASD controls with collision detection
- **Basic Photography**: Left-click to take pictures (console output only)
- **Initial Texturing**: Applied textures to terrain
- **Environment Setup**: Sky color and basic lighting

### Planned (Upcoming Weeks)

- **Deer AI**: Movement patterns, detection systems
- **Environment**: Trees, rocks, water features
- **Advanced Photography**: Line-of-sight checks, subject detection
- **Scoring System**: Points for deer photographs
- **UI Elements**: HUD, menus, score display
- **Multiplayer Support**: Network-based gameplay

## Known Issues

- Terrain texture tiling pattern is visible
- Heightmap could use more definition for better terrain features
- No trees or other environment objects yet
- Collision is limited to a simple ground plane
- Photography system only prints to console

## Development Timeline

| Week | Focus | Status |
|------|-------|--------|
| 1 | Core Setup | ✅ Completed |
| 2 | Game Entities | 🚧 Planned |
| 3 | Game Mechanics | 🚧 Planned |
| 4 | Networking | 🚧 Planned |
| 5 | Refinement | 🚧 Planned |
| 6 | Finalization | 🚧 Planned |

## Credits

- **Panda3D**: 3D game engine - [https://www.panda3d.org/](https://www.panda3d.org/)
- **Advanced Object-Oriented Programming Course**: TU Wien

## License

This project is created for educational purposes as part of the Advanced Object-Oriented Programming course at TU Wien.
