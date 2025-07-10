"
Position class for handling grid coordinates in the deer hunting game.
Represents a location on the game grid with x and y coordinates.
"

Object subclass: #Position
    instanceVariableNames: 'x y'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Core'

"Instance creation"
Position class >> x: xCoord y: yCoord
    "Create a new position with the given coordinates"
    ^ self new x: xCoord y: yCoord

"Initialization"
Position >> x: xCoord y: yCoord
    "Initialize this position with coordinates"
    x := xCoord.
    y := yCoord

"Accessing"
Position >> x
    "Return the x coordinate"
    ^ x

Position >> y
    "Return the y coordinate"
    ^ y

Position >> x: newX
    "Set the x coordinate"
    x := newX

Position >> y: newY
    "Set the y coordinate"
    y := newY

"Comparing"
Position >> = aPosition
    "Return true if this position equals another position"
    ^ (aPosition isKindOf: Position) and: [
        (self x = aPosition x) and: [self y = aPosition y]]

Position >> hash
    "Return hash value for this position"
    ^ (x hash bitXor: y hash)

"Arithmetic"
Position >> + aPosition
    "Add this position to another position"
    ^ Position x: (x + aPosition x) y: (y + aPosition y)

Position >> - aPosition
    "Subtract another position from this position"
    ^ Position x: (x - aPosition x) y: (y - aPosition y)

"Distance calculations"
Position >> distanceTo: aPosition
    "Calculate Manhattan distance to another position"
    ^ (self x - aPosition x) abs + (self y - aPosition y) abs

Position >> isAdjacentTo: aPosition
    "Check if this position is adjacent to another position"
    ^ (self distanceTo: aPosition) = 1

"Directions"
Position >> north
    "Return position one step north"
    ^ Position x: x y: y - 1

Position >> south
    "Return position one step south"
    ^ Position x: x y: y + 1

Position >> east
    "Return position one step east"
    ^ Position x: x + 1 y: y

Position >> west
    "Return position one step west"
    ^ Position x: x - 1 y: y

Position >> moveInDirection: direction
    "Move in the given direction (symbol)"
    direction = #north ifTrue: [^ self north].
    direction = #south ifTrue: [^ self south].
    direction = #east ifTrue: [^ self east].
    direction = #west ifTrue: [^ self west].
    ^ self

"Testing"
Position >> isValidInWorld: aGameWorld
    "Check if this position is valid within the game world bounds"
    ^ (x >= 1) and: [x <= aGameWorld width] and: 
      [y >= 1] and: [y <= aGameWorld height]

"Printing"
Position >> printOn: aStream
    "Print a readable representation"
    aStream nextPutAll: '('; print: x; nextPutAll: ','; print: y; nextPut: $)