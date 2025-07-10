# Deer Hunting Game - Smalltalk Implementation

**Assignment:** Smalltalk OOP Demonstration  

## Project Overview

A terminal-based deer hunting game implemented in Smalltalk to demonstrate core Object-Oriented Programming concepts including inheritance, polymorphism, message passing, and dynamic typing.

## Features

- **Grid-based game world** (10x10 ASCII representation)
- **Intelligent deer AI** with flee behavior
- **Line-of-sight photography** mechanics
- **Real-time game updates** with turn-based controls
- **Complete OOP hierarchy** showcasing Smalltalk principles

## Classes Implemented

1. **Position** - Grid coordinates and movement calculations
2. **GameObject** - Abstract base class for all game entities
3. **Hunter** - Player character with movement and photography
4. **Deer** - AI animals with alert levels and flee behavior
5. **Obstacle/Tree/Rock/Bush** - Environmental objects with different properties
6. **GameWorld** - Game state management and object coordination
7. **Game** - Main controller and testing framework
8. **GameDisplay** - ASCII art terminal interface

## OOP Concepts Demonstrated

- **Inheritance:** GameObject hierarchy with specialized subclasses
- **Polymorphism:** Same messages (symbol, update) produce different behaviors
- **Message Passing:** `hunter moveInDirection: #north` instead of method calls
- **Encapsulation:** Instance variables protected with accessor methods
- **Dynamic Typing:** Duck typing with `isPlayer`, `isDeer` testing methods
- **Blocks & Closures:** `[:obj | obj isDeer]` for functional programming
- **Collections:** Smalltalk's powerful collection iteration methods

## Installation & Demo

1. Open Squeak Smalltalk
2. Create package: `DeerHuntingGame`
3. File in all source files in order
4. Run demo script: `DemoScript.st`

## Game Controls

- **W/A/S/D:** Move North/West/South/East
- **SPACE:** Take photograph
- **Q:** Quit game

## Technical Highlights

- **AI Behavior:** Deer alert levels increase with hunter proximity
- **Line-of-sight:** Photography requires clear vision path
- **Collision Detection:** Objects block movement appropriately
- **State Management:** Game world updates after each turn