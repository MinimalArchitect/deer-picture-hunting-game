"
Game class that manages the main game loop and overall game state.
This is the main controller for the deer hunting game.
"

Object subclass: #Game
    instanceVariableNames: 'world timeLeft gameRunning'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Core'

"Instance creation"
Game class >> new
    "Create a new game instance"
    ^ super new initialize

"Initialization"
Game >> initialize
    "Initialize the game"
    super initialize.
    world := GameWorld width: 10 height: 10.
    world setupSimpleWorld.
    timeLeft := 60.
    gameRunning := false

"Accessing"
Game >> world
    "Return the game world"
    ^ world

Game >> timeLeft
    "Return the time left in seconds"
    ^ timeLeft

Game >> isRunning
    "Return true if the game is running"
    ^ gameRunning

Game >> player
    "Return the hunter"
    ^ world player

"Game control"
Game >> start
    "Start the game"
    gameRunning := true.
    self showInstructions.
    Transcript show: 'Game started! Good luck hunting!'; cr

Game >> stop
    "Stop the game"
    gameRunning := false.
    self showFinalScore

Game >> showInstructions
    "Display game instructions"
    Transcript clear.
    Transcript show: 'Deer Picture Hunting Game - Smalltalk Version'; cr.
    Transcript show: '============================================'; cr; cr.
    Transcript show: 'Instructions:'; cr.
    Transcript show: '  W/A/S/D = Move North/West/South/East'; cr.
    Transcript show: '  SPACE = Take Photo'; cr.
    Transcript show: '  Q = Quit Game'; cr; cr.
    Transcript show: 'Legend:'; cr.
    Transcript show: '  ↑↓←→ = Hunter (showing direction)'; cr.
    Transcript show: '  D = Deer'; cr.
    Transcript show: '  X = Photographed Deer'; cr.
    Transcript show: '  T = Tree'; cr.
    Transcript show: '  R = Rock'; cr.
    Transcript show: '  B = Bush'; cr.
    Transcript show: '  . = Empty Space'; cr; cr

Game >> showFinalScore
    "Display the final score"
    Transcript cr.
    Transcript show: '=== GAME OVER ==='; cr.
    Transcript show: 'Final Score: ', world player score printString, 
                    ' out of ', world totalDeer printString, ' deer photographed'; cr.
    Transcript show: 'Photos taken: ', world player photosTaken printString; cr.
    
    world photographedDeerCount = world totalDeer ifTrue: [
        Transcript show: 'Perfect game! You photographed all the deer!'; cr
    ]

"Game loop and input"
Game >> playGame
    "Main game loop"
    | display input |
    display := GameDisplay new.
    display world: world.
    
    self start.
    display showWorld.
    
    [gameRunning] whileTrue: [
        Transcript cr.
        Transcript show: 'Enter command (W/A/S/D/SPACE/Q): '.
        input := self getInput.
        self processInput: input.
        world update.
        display showWorld
    ].
    
    self stop

Game >> getInput
    "Get input from user (simplified for demo)"
    ^ 'w'

Game >> processInput: input
    "Process user input"
    | hunter moved |
    hunter := world player.
    
    input = 'w' ifTrue: [moved := hunter moveInDirectionWithBounds: #north].
    input = 's' ifTrue: [moved := hunter moveInDirectionWithBounds: #south].
    input = 'a' ifTrue: [moved := hunter moveInDirectionWithBounds: #west].
    input = 'd' ifTrue: [moved := hunter moveInDirectionWithBounds: #east].
    input = ' ' ifTrue: [
        hunter takePhotoAdvanced.
        Transcript show: '*CLICK* Photo taken!'; cr
    ].
    input = 'q' ifTrue: [gameRunning := false].
    
    moved ifNil: [moved := true].
    moved ifFalse: [
        Transcript show: 'Cannot move there!'; cr
    ]

"Testing methods"
Game >> testBasicFunctionality
    "Test basic functionality of all classes"
    | testResults |
    testResults := OrderedCollection new.
    
    testResults add: self testPosition.
    testResults add: self testGameObjects.
    testResults add: self testGameWorld.
    
    ^ testResults

Game >> testPosition
    "Test Position class functionality"
    | pos1 pos2 |
    Transcript show: 'Testing Position class...'; cr.
    
    pos1 := Position x: 3 y: 4.
    pos2 := Position x: 5 y: 6.
    
    Transcript show: '  Position creation: ', pos1 printString; cr.
    Transcript show: '  Distance calculation: ', (pos1 distanceTo: pos2) printString; cr.
    Transcript show: '  Direction movement: ', pos1 north printString; cr.
    
    ^ 'Position tests completed'

Game >> testGameObjects
    "Test GameObject hierarchy"
    | hunter deer tree |
    Transcript show: 'Testing GameObject hierarchy...'; cr.
    
    hunter := Hunter at: (Position x: 1 y: 1) inWorld: world.
    deer := Deer at: (Position x: 3 y: 3) inWorld: world.
    tree := Tree at: (Position x: 2 y: 2) inWorld: world.
    
    Transcript show: '  Hunter symbol: ', hunter symbol printString; cr.
    Transcript show: '  Deer symbol: ', deer symbol printString; cr.
    Transcript show: '  Tree symbol: ', tree symbol printString; cr.
    Transcript show: '  Tree blocks movement: ', tree blocksMovement printString; cr.
    
    ^ 'GameObject tests completed'

Game >> testGameWorld
    "Test GameWorld functionality"
    Transcript show: 'Testing GameWorld...'; cr.
    
    Transcript show: '  World size: ', world width printString, 'x', world height printString; cr.
    Transcript show: '  Total objects: ', world objects size printString; cr.
    Transcript show: '  Total deer: ', world totalDeer printString; cr.
    Transcript show: '  Hunter position: ', world player position printString; cr.
    
    ^ 'GameWorld tests completed'