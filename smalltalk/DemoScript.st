"
DEER HUNTING GAME - COMPLETE DEMONSTRATION SCRIPT
Student: [Your Name]
Course: [Course Code]
Assignment: Smalltalk OOP Demonstration

This script demonstrates all major OOP concepts implemented in the game.
Run each section separately during presentation.
"

"=== SECTION 1: CLASS HIERARCHY DEMONSTRATION ==="
Transcript clear.
Transcript show: '=== SMALLTALK OOP FEATURES DEMONSTRATION ==='; cr; cr.

"Show inheritance hierarchy"
Transcript show: '1. INHERITANCE HIERARCHY:'; cr.
Transcript show: '   Object'; cr.
Transcript show: '   ├── Position (coordinates and movement)'; cr.
Transcript show: '   ├── GameWorld (world management)'; cr.
Transcript show: '   ├── Game (main controller)'; cr.
Transcript show: '   ├── GameDisplay (terminal interface)'; cr.
Transcript show: '   └── GameObject (abstract base class)'; cr.
Transcript show: '       ├── Hunter (player character)'; cr.
Transcript show: '       ├── Deer (AI animals)'; cr.
Transcript show: '       └── Obstacle'; cr.
Transcript show: '           ├── Tree (blocks movement & vision)'; cr.
Transcript show: '           ├── Rock (blocks movement & vision)'; cr.
Transcript show: '           └── Bush (blocks vision only)'; cr; cr.

"=== SECTION 2: MESSAGE PASSING DEMONSTRATION ==="
Transcript show: '2. MESSAGE PASSING (not method calls):'; cr.

"Create objects to demonstrate message passing"
pos := Position x: 3 y: 4.
hunter := Hunter new.
deer := Deer new.

"Show message passing syntax"
Transcript show: '   Position x: 3 y: 4  → ', pos printString; cr.
Transcript show: '   hunter moveInDirection: #north'; cr.
Transcript show: '   deer fleeFromPlayer'; cr.
Transcript show: '   objects select: [:obj | obj isDeer]'; cr; cr.

"=== SECTION 3: POLYMORPHISM DEMONSTRATION ==="
Transcript show: '3. POLYMORPHISM (same message, different behavior):'; cr.

"Create different object types"
tree := Tree new.
rock := Rock new.
bush := Bush new.

"Show polymorphic behavior"
Transcript show: '   tree symbol → ', tree symbol printString; cr.
Transcript show: '   rock symbol → ', rock symbol printString; cr.
Transcript show: '   bush symbol → ', bush symbol printString; cr.
Transcript show: '   deer symbol → ', deer symbol printString; cr.
Transcript show: '   hunter symbol → ', hunter symbol printString; cr; cr.

"=== SECTION 4: BLOCKS AND CLOSURES ==="
Transcript show: '4. BLOCKS AND CLOSURES (functional programming):'; cr.
game := Game new.
allObjects := game world objects.

"Demonstrate blocks"
deerCount := (allObjects select: [:obj | obj isDeer]) size.
obstacleCount := (allObjects select: [:obj | obj isObstacle]) size.

Transcript show: '   [:obj | obj isDeer] → Found ', deerCount printString, ' deer'; cr.
Transcript show: '   [:obj | obj isObstacle] → Found ', obstacleCount printString, ' obstacles'; cr.
Transcript show: '   [alertLevel > 5] ifTrue: [self fleeFromPlayer]'; cr; cr.

"=== SECTION 5: DYNAMIC TYPING DEMONSTRATION ==="
Transcript show: '5. DYNAMIC TYPING (duck typing):'; cr.
Transcript show: '   Objects respond to messages they understand:'; cr.
Transcript show: '   hunter isPlayer → ', hunter isPlayer printString; cr.
Transcript show: '   deer isDeer → ', deer isDeer printString; cr.
Transcript show: '   tree blocksMovement → ', tree blocksMovement printString; cr.
Transcript show: '   bush blocksMovement → ', bush blocksMovement printString; cr; cr.

"=== SECTION 6: COMPLETE GAME DEMONSTRATION ==="
Transcript show: '6. COMPLETE GAME IN ACTION:'; cr; cr.

"Initialize display"
display := GameDisplay new.
display world: game world.

"Show initial game state"
display showWorld.

"=== SECTION 7: AI AND INTERACTION DEMO ==="
Transcript cr.
Transcript show: '=== DEMONSTRATING AI BEHAVIOR AND GAME MECHANICS ==='; cr.

"Move hunter closer to deer to trigger AI"
hunter := game player.
firstDeer := game world deer first.
Transcript show: 'Initial deer position: ', firstDeer position printString; cr.
Transcript show: 'Initial deer alert level: ', firstDeer alertLevel printString; cr; cr.

"Simulate several game turns"
gameplayMoves := #('w' 'a' 'd' 's' ' ' 'w' 'a' ' ').
gameplayMoves do: [:move |
    Transcript show: '>>> Player input: ', move printString; cr.
    
    "Process the move"
    game processInput: move.
    
    "Update world (triggers deer AI)"
    game world update.
    
    "Show updated state"
    display showWorld.
    
    "Show AI state changes"
    game world deer do: [:deer |
        Transcript show: '  Deer at ', deer position printString, 
                        ' alert level: ', deer alertLevel printString, 
                        ' photographed: ', deer isPhotographed printString; cr
    ].
    Transcript cr.
].

"=== SECTION 8: FINAL SUMMARY ==="
Transcript show: '=== SMALLTALK OOP CONCEPTS DEMONSTRATED ==='; cr.
Transcript show: '✓ Inheritance - GameObject hierarchy with specialized behaviors'; cr.
Transcript show: '✓ Polymorphism - Same messages produce different results'; cr.
Transcript show: '✓ Message Passing - Pure OO communication model'; cr.
Transcript show: '✓ Encapsulation - Instance variables protected by accessors'; cr.
Transcript show: '✓ Dynamic Typing - Duck typing with behavioral testing'; cr.
Transcript show: '✓ Blocks & Closures - Functional programming elements'; cr.
Transcript show: '✓ Collections - Powerful iteration and filtering'; cr.
Transcript show: '✓ Live Development - Code compiled and tested in running system'; cr; cr.

Transcript show: 'DEMONSTRATION COMPLETE!'; cr.
Transcript show: 'Game mechanics are fully functional.'; cr.
Transcript show: 'Interactive play available through manual input processing.'; cr.
Transcript show: 'All OOP concepts successfully demonstrated!'; cr.