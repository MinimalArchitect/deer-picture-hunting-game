# Development Roadmap

## Week 1-2: Core Python Implementation

### ✅ Basic 2D Grid-Based Game (Completed)
We've implemented a foundational grid-based game using Python and Pygame. This includes:
- Grid-based movement system with four directional controls
- Basic deer AI that reacts to player proximity
- Simple photography mechanic that detects deer in the player's line of sight
- Environment with obstacles (trees, rocks, bushes) that affect movement and visibility
- Timer and scoring system

### ✅ Main Menu Screen (Completed)
The main menu provides entry points to different game modes and settings:
- **Implementation completed**:
  - Created `Menu` and `Button` classes for UI interaction
  - Implemented screen state management with mouse hover effects
  - Added event handling for button clicks
  - Set up menu-to-game state transitions
- **Current features**:
  - Single Player button (starts game)
  - Host Game button (currently starts single player mode)
  - Join Game button (currently starts single player mode)
  - Options button (placeholder screen with "Coming Soon")
  - High Scores button (placeholder screen with "Coming Soon")
  - Exit button (quits application)
- **Menu flow**:
  - ESC key returns from game to menu
  - Game over screen transitions back to menu
  - Clean state management between screens
- **Future improvements**:
  - Implement actual multiplayer functionality for Host/Join
  - Complete Options and High Scores screens

### ⬜ High Score System
The high score system will track and display top performances:
- **Data storage**: Use JSON file format to persist scores between sessions
- **Score structure**: Store player name, score, date/time, and game settings
- **UI components**: 
  - Score display at end of game
  - Name entry for high scores
  - Sortable high score table
- **Technical implementation**: Create a `ScoreManager` class that handles reading, writing, and sorting score data

### ⬜ Networking
The networking layer will enable multiplayer functionality where multiple hunters can play in the same environment:

#### Client-Server Architecture
- **Technology choice**: Use Python's `socket` library or higher-level networking library like `Pyro4`
- **Server responsibilities**:
  - Maintain authoritative game state
  - Process player inputs
  - Update and broadcast world state
  - Handle deer AI centrally
  - Track scoring and game progress
- **Client responsibilities**:
  - Send player inputs to server
  - Render game state received from server
  - Handle local UI and controls
  - Display other players

#### Player Synchronization
- **State synchronization**: 
  - Server sends periodic state updates (positions, scores, game time)
  - Client implements interpolation between updates to ensure smooth movement
  - Use delta compression to minimize network traffic
- **Latency handling**:
  - Implement client-side prediction for responsive movement
  - Server reconciliation to correct client prediction errors
  - Timestamp-based synchronization

#### Join/Host Game Functionality
- **Host game flow**:
  - Player selects "Host Game" from menu
  - Creates game configuration (time limit, difficulty, etc.)
  - Server begins listening for connections
  - Lobby screen shows connected players
  - Host can start game when ready
- **Join game flow**:
  - Player selects "Join Game" from menu
  - Enters host's IP address or discovers hosts on local network
  - Connects to server and enters lobby
  - Waits for host to start game

#### Multiple Hunter Representation
- **Visual distinction**: Different colors or sprites for each hunter
- **Collision handling**: Prevent hunters from walking through each other
- **Photography interactions**: 
  - Detect when a hunter photographs another hunter (disqualification)
  - Ensure deer photographs are properly attributed to the correct hunter
- **Score tracking**: Individual score tracking for each player

## Week 3: Polish and Enhancements

### ⬜ Different Deer Types
We'll implement various types of deer with distinct behaviors and characteristics:
- **Common Deer**: Standard behavior, worth 1 point
- **Rare Deer**: Moves faster and is more alert, worth 3 points
- **Shy Deer**: Always stays far from players, worth 5 points
- **Curious Deer**: Occasionally approaches players, worth 2 points
- **Implementation details**: Create subclasses of the base `Deer` class, overriding movement and update methods to implement unique behaviors

### ⬜ Difficulty Levels
Multiple difficulty settings to accommodate different skill levels:
- **Easy**: 
  - Deer are less sensitive to player movement
  - Longer time limit
  - Larger photo capture range
- **Normal**: Balanced difficulty with standard parameters
- **Hard**: 
  - Deer have heightened awareness
  - Shorter time limit
  - Narrower photo capture range
  - More obstacles in the environment
- **Technical approach**: Create a `DifficultyManager` class that adjusts game parameters based on selected difficulty

### ⬜ Visual Indicators for Photo Range
Implement visual feedback for the photography mechanic:
- **Line of sight indicator**: Visual line or cone showing the direction and range of photos
- **Photo flash effect**: Visual feedback when a photo is taken
- **Capture preview**: Small overlay showing what was captured in the photo
- **Implementation**: Use Pygame's drawing functions to create these visual elements in the game's render phase

### ⬜ Sound Effects
Add audio feedback to enhance the game experience:
- **Movement sounds**: Footsteps that vary based on terrain
- **Camera sounds**: Shutter click when taking photos
- **Ambient sounds**: Forest background noises
- **Alert sounds**: When deer detect the player
- **Technical details**: Use Pygame's mixer module to load and play sound effects
- **Sound design considerations**: Volume balancing and spatial audio for immersion

### ⬜ Final Gameplay Balancing
Fine-tune game parameters for optimal player experience:
- **Testing methodology**: Playtest with various player types and collect feedback
- **Key balance factors**:
  - Deer spawn rate and distribution
  - Player and deer movement speeds
  - Detection radii for different deer types
  - Time limits for different difficulty levels
  - Scoring system adjustments
- **Implementation**: Create configuration file for easy adjustment of balance parameters

## Week 4: Smalltalk Implementation

### ⬜ Port Core Game Mechanics to Smalltalk
Transfer the fundamental game logic to Smalltalk:
- **Development environment**: Use Squeak Smalltalk as recommended in the assignment
- **Core classes to port**:
  - GameObject (base class)
  - Player
  - Deer (and variants)
  - GameMap
  - Game (main controller)
- **Adaptation strategy**: Start with basic structure and incrementally add functionality
- **Technical considerations**: Leverage Smalltalk's dynamic typing and message-passing for clean OOP design

### ⬜ Adapt to Smalltalk UI Patterns
Modify the user interface to work within Smalltalk's environment:
- **UI toolkit**: Use Morphic for graphical elements
- **Event handling**: Implement Smalltalk-style event subscription
- **Window management**: Create proper Smalltalk windows and views
- **Input handling**: Adapt keyboard and mouse controls to Smalltalk's event system
- **Technical approach**: Study existing Smalltalk games as references for UI implementation

### ⬜ Ensure Basic Gameplay Works
Focus on core functionality before advanced features:
- **Testing strategy**: Implement unit tests for critical game mechanics
- **Minimum viable features**:
  - Grid-based movement
  - Basic deer behavior
  - Simple photography mechanism
  - Score tracking
- **Technical challenges**: Adapt to Smalltalk's performance characteristics and memory management

## Week 5: Eiffel Implementation

### ⬜ Port Core Game to Eiffel
Transfer the game logic to Eiffel, focusing on language-specific features:
- **Development environment**: Use EiffelStudio as recommended in the assignment
- **Class hierarchy**: Adapt the object model to Eiffel's inheritance system
- **Feature implementation**: Convert methods to Eiffel features
- **Technical considerations**: Adapt to Eiffel's static typing system

### ⬜ Implement Design-by-Contract Features
Leverage Eiffel's signature feature for better code reliability:
- **Preconditions**: Define what must be true before methods execute
  - Movement methods check for valid positions
  - Photography methods verify proper direction and state
- **Postconditions**: Define what must be true after methods execute
  - Ensure state consistency after movement
  - Verify photo results are properly recorded
- **Class invariants**: Define what must always be true for objects
  - Player always in valid grid position
  - Game score always non-negative
  - Deer always in proper behavioral state
- **Technical benefits**: Use contracts to catch bugs early and document expected behavior

### ⬜ Add Terminal Fallback if Needed
Prepare for potential graphical limitations in Eiffel:
- **Text-based interface**: Design a terminal representation of the game state
  - ASCII art for the grid and entities
  - Text commands for player actions
  - Clear screen and redraw for animation
- **Implementation approach**: Create adapter classes that switch between graphical and text modes
- **Technical considerations**: Handle timing and input differently for terminal mode

## Week 6: Finalization

### ⬜ Prepare Comparison Documentation
Document the differences between implementations:
- **Comparative analysis**:
  - Language syntax differences
  - OOP feature comparison
  - Performance characteristics
  - Development experience
  - Code maintainability
- **Code mapping**: Show how the same concepts are implemented across languages
- **Lessons learned**: Document insights gained from each implementation

### ⬜ Create Presentation Slides
Prepare materials for the final presentation:
- **Key sections**:
  - Project overview and requirements
  - Design decisions and architecture
  - Implementation differences across languages
  - Technical challenges and solutions
  - Live demonstration plan
  - Conclusions and lessons learned
- **Visual elements**: Include screenshots, code snippets, and diagrams

### ⬜ Ready Demonstration of All Versions
Prepare to showcase all three implementations:
- **Demo setup**: Configure environments for quick switching between versions
- **Demonstration script**: Plan specific features to highlight in each version
- **Fallback plans**: Prepare for potential technical issues during presentation
- **Technical needs**: Ensure all necessary software is installed and configured

### ⬜ Complete Submission Materials
Finalize all required deliverables:
- **Code repositories**: Clean up and organize code for all three implementations
- **Documentation**: Complete READMEs and technical documentation
- **User guides**: Instructions for installing and running each version
- **Answers to assignment questions**: Prepare responses to specific questions in the assignment
- **Reflection document**: Summarize the experience and lessons learned
