# Deer Picture Hunting Game (2D Grid-Based Version)

<table>
  <tr>
    <td><img src="screenshots/main-menu.png" width="230"/></td>
    <td><img src="screenshots/game_preview.png" width="230"/></td>
  </tr>
  <tr>
    <td align="center">Main Menu</td>
    <td align="center">Gameplay</td>
  </tr>
  <tr>
    <td><img src="screenshots/game_preview_flickering_hunter.png" width="230"/></td>
    <td><img src="screenshots/name-dialog.png" width="230"/></td>
    <td><img src="screenshots/game_over-new_record-screen.png" width="230"/></td>
  </tr>
  <tr>
    <td align="center">Gameplay with flickering hunter</td>
    <td align="center">Name dialog box</td>
    <td align="center">Game Over/New Record</td>
  </tr>
<tr>
    <td><img src="screenshots/choose_level_preview.png" width="230"/></td>
    <td><img src="screenshots/options_menu.png" width="230"/></td>
  </tr>
  <tr>
    <td align="center">Choose Level Preview</td>
    <td align="center">Options menu</td>
  </tr>
<tr>
    <td><img src="screenshots/scores_menu1.png" width="230"/></td>
    <td><img src="screenshots/scores_menu2.png" width="230"/></td>
    <td><img src="screenshots/high_scores_menu.png" width="230"/></td>
  </tr>
  <tr>
    <td align="center">Scores - Level-1</td>
    <td align="center">Scores - Level-2</td>
    <td align="center">High Scores - all levels</td>
  </tr>
</table>

A simplified 2D grid-based implementation of the Deer Picture Hunting Game developed for the Advanced Object-Oriented Programming course at TU Wien.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Implementation Details](#implementation-details)
- [Architecture](#architecture)
- [Code Structure](#code-structure)
- [Development Status](#development-status)
- [Assignment Context](#assignment-context)

## Overview

Deer Picture Hunting Game is a grid-based 2D game where you play as a wildlife photographer attempting to take pictures of deer in a forest environment. The deer react to your presence, attempting to flee when you get too close. Navigate the environment carefully, avoid alerting the deer, and capture as many unique photographs as possible before time runs out.

This version uses a simplified grid-based approach to focus on the core game mechanics and object-oriented programming principles rather than complex graphics and physics.

## Current Implementation Status

✅ **Phase 1 & 2 Complete**: Core game with clean state machine architecture  
🚧 **Phase 3**: Specialized states (Game Over, Level Selection, High Score)  
⏳ **Phase 4**: Networking implementation  
⏳ **Phase 5**: Smalltalk port  
⏳ **Phase 6**: Eiffel port  

## Features

### 🎮 **Core Gameplay**
- **Single Player Mode** with full functionality
- **20 Predefined Levels** with increasing difficulty
- **Dynamic Deer AI**: Proximity-based alert and flee behaviors
- **Photography Mechanic**: Directional picture taking
- **Environmental Obstacles**: Trees, rocks, and bushes affecting movement and vision

### 🏗️ **Architecture**
- **Clean State Machine**: Modular state-based architecture ready for networking
- **Professional OOP Design**: Proper inheritance, encapsulation, and polymorphism
- **Extensible Framework**: Easy to add new game modes and features

### 💾 **Persistence & UI**
- **Advanced High Score System**: Per-level tracking with player names and timestamps
- **Complete Menu System**: Main menu, options, level selection, high scores
- **Game State Management**: Pause, resume, level progression
- **Sound System**: Toggle-able sound effects
- **Visual Polish**: Animated hunter highlighting, smooth transitions

## Installation

### Prerequisites
- Python 3.8 or higher
- `pygame` library

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/MinimalArchitect/deer-picture-hunting-game.git
   cd deer-picture-hunting-game
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. Install required packages:
   ```bash
   pip install pygame
   ```

4. Run the game:
   ```bash
   python main.py
   ```

## How to Play

- **Main Menu**: Click on options with your mouse
- **Arrow Keys**: Move your photographer (hunter) around the map
- **Space**: Take a picture in the direction you're facing
- **ESC**: Pause game, return to main menu, or exit
- **Goal**: Photograph as many unique deer as possible before time runs out
- **Scoring**: Each unique deer photographed awards 1 point

### Environment Elements

- **🌲 Trees**: Block movement and vision
- **🗿 Rocks**: Block movement and vision  
- **🌿 Bushes**: Allow movement but block vision
- **🦌 Deer**: Your photography targets
- **🏃 Hunter**: Player character (points in facing direction)

## Implementation Details

The game showcases advanced object-oriented programming principles:

### 🏗️ **Architecture Patterns**
- **State Machine Pattern**: Clean separation of game states (Menu, Playing, Paused, etc.)
- **Observer Pattern**: Event-driven UI and game logic
- **Strategy Pattern**: Different deer AI behaviors
- **Template Method**: Consistent state lifecycle management

### 🧱 **OOP Design**
- **Inheritance Hierarchies**: GameObject → Player/Deer, GameState → MenuState/PlayingState
- **Polymorphism**: Different entities with unified interfaces
- **Encapsulation**: Proper data hiding and interface design
- **Abstraction**: Clean abstractions for game logic and rendering

### 💾 **Data Management**
- **Persistent Storage**: JSON-based high score system with full metadata
- **State Persistence**: Game state preservation across pause/resume
- **Configuration Management**: Centralized game settings and level data

## Architecture

### State Machine Design
```
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ Menu State  │───▶│ Level Selection  │───▶│ Playing State   │
└─────────────┘    └──────────────────┘    └─────────────────┘
       ▲                                            │
       │            ┌─────────────────┐             ▼
       └────────────│ Paused State    │◄────────────┤
                    └─────────────────┘             │
       ┌─────────────────────────────────────────────┘
       ▼
┌─────────────────┐    ┌──────────────────┐
│ Game Over State │───▶│ High Score State │
└─────────────────┘    └──────────────────┘
```

### Class Hierarchy
```
GameState (Abstract)
├── TransitionableState
│   ├── MenuState
│   ├── PlayingState
│   └── PausedState
└── GameOverState
    ├── LevelSelectionState
    └── HighScoreState

GameObject (Abstract)
├── Player
└── Deer

StateMachine
└── manages all state transitions
```

## Code Structure

```
assets/                 # Game assets
├── textures/           # Sprite images
└── sounds/             # Audio files
screenshots/            # Documentation images
src/
├── core/               # Core engine components
│   ├── game.py         # Main game loop with state machine
│   ├── game_map.py     # Level and terrain management
│   ├── game_state.py   # Abstract state base classes
│   └── state_machine.py # State transition manager
├── entity/             # Game entities
│   ├── game_object.py  # Base entity class
│   ├── player.py       # Player character and controls
│   └── deer.py         # Deer AI and behavior
├── states/             # 🆕 State implementations
│   ├── menu_state.py   # Main menu logic
│   ├── playing_state.py # Core gameplay state
│   └── paused_state.py # Pause menu state
├── ui/                 # User interface components
│   ├── button.py       # Interactive buttons
│   ├── menu.py         # Menu system
│   ├── high_score_screen.py # Score display
│   └── name_input_dialog.py # Name entry
└── util/               # Utilities and configuration
    ├── color.py        # Color constants
    ├── config.py       # Game configuration
    ├── score_manager.py # High score management
    ├── sound.py        # Audio management
    └── texture.py      # Asset loading
main.py                 # Entry point
test_foundation.py      # 🆕 State machine testing
level_scores.json       # Persistent high scores
```

### 🆕 **New Architecture Benefits**
- **Single Responsibility**: Each state handles only its specific functionality
- **Clean Transitions**: Proper state lifecycle with enter/exit methods
- **Networking Ready**: Single main loop can handle network events
- **Extensible**: Easy to add new states (lobby, multiplayer, etc.)
- **Testable**: Modular design allows for unit testing
- **Maintainable**: Clear separation of concerns

## Development Status

### ✅ **Completed Features**
- **Core Gameplay**: Full single-player experience with 20 levels
- **State Machine Architecture**: Professional state management system
- **High Score System**: Complete with player names, timestamps, and persistence
- **UI System**: Comprehensive menu system with all screens
- **Audio System**: Sound effects with toggle functionality
- **Level System**: 20 predefined levels with increasing difficulty

### 🚧 **In Progress**
- **Specialized States**: Implementing remaining states (Game Over, Level Selection)
- **State Integration**: Connecting new state machine with existing UI components

### ⏳ **Planned Features**
- **Networking Layer**: Client-server multiplayer implementation
- **Lobby System**: Multiplayer game setup and management
- **Advanced AI**: More sophisticated deer behaviors
- **Performance Optimization**: Efficient rendering and game logic

## Development Timeline

This project represents the first phase of a three-part assignment:

### **Phase 1: Python Implementation** (Current)
- ✅ **Foundation**: Core gameplay and architecture
- ✅ **State Machine**: Professional state management
- 🚧 **Polish**: Final UI integration and testing
- ⏳ **Networking**: Multiplayer functionality

### **Phase 2: Smalltalk Implementation** (Upcoming)
- Port core game logic to Smalltalk
- Explore Smalltalk's unique OOP features
- Adapt UI to Smalltalk's development environment

### **Phase 3: Eiffel Implementation** (Upcoming)
- Implement in Eiffel with design-by-contract
- Utilize Eiffel's assertion and contract capabilities
- Create terminal-based fallback if needed

Each implementation explores different object-oriented programming paradigms and language-specific features.

## Assignment Context

This game is developed as part of the "Advanced Object-Oriented Programming" course at TU Wien. The assignment demonstrates:

1. **Networked OOP Application**: Python implementation with clean architecture
2. **Language Comparison**: Exploring OOP features across three languages
3. **Design Patterns**: Professional software architecture patterns
4. **Software Engineering**: Version control, testing, and documentation

The project showcases advanced OOP concepts including state machines, design patterns, and architectural principles that scale to real-world software development.

---