"
GameDisplay class for ASCII art representation of the game world.
Handles terminal interface and visual game state display.
"

Object subclass: #GameDisplay
    instanceVariableNames: 'world'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Core'

"Initialization"
GameDisplay >> world: aGameWorld
    "Set the game world to display"
    world := aGameWorld

"Display methods"
GameDisplay >> showWorld
    "Display the complete game state"
    | grid |
    self showStatus.
    Transcript cr.
    
    grid := self createGrid.
    self displayGrid: grid.
    
    Transcript cr.
    self showLegend.
    self showControls

GameDisplay >> createGrid
    "Create a 2D array representing the game world"
    | grid |
    grid := Array new: world height.
    1 to: world height do: [:y |
        grid at: y put: (Array new: world width withAll: $.)
    ].
    
    world objects do: [:obj |
        grid at: obj y put: (grid at: obj y) copy.
        (grid at: obj y) at: obj x put: obj symbol
    ].
    
    ^ grid

GameDisplay >> displayGrid: grid
    "Display the game grid with coordinates"
    Transcript show: '    1 2 3 4 5 6 7 8 9 10'; cr.
    Transcript show: '  +'.
    1 to: world width do: [:i | Transcript show: '-'].
    Transcript show: '+'; cr.
    
    1 to: world height do: [:y |
        y < 10 ifTrue: [Transcript show: ' '].
        Transcript show: y printString, '| '.
        1 to: world width do: [:x |
            Transcript nextPut: ((grid at: y) at: x).
            Transcript show: ' '
        ].
        Transcript show: '|'; cr
    ].
    
    Transcript show: '  +'.
    1 to: world width do: [:i | Transcript show: '-'].
    Transcript show: '+'; cr

GameDisplay >> showStatus
    "Display game status information"
    | hunter |
    hunter := world player.
    Transcript clear.
    Transcript show: 'Deer Picture Hunting Game - Smalltalk Version'; cr.
    Transcript show: '==============================================='; cr; cr.
    Transcript show: 'Score: ', hunter score printString, '/', world totalDeer printString, ' deer photographed'; cr.
    Transcript show: 'Photos taken: ', hunter photosTaken printString; cr.
    Transcript show: 'Hunter position: ', hunter position printString, ' facing ', hunter direction printString; cr

GameDisplay >> showLegend
    "Display the game legend"
    Transcript show: 'Legend: ', world player symbol printString, '=Hunter D=Deer X=Photographed T=Tree R=Rock B=Bush .=Empty'; cr

GameDisplay >> showControls
    "Display game controls"
    Transcript show: 'Commands: W/A/S/D=Move, SPACE=Take Photo, Q=Quit'; cr