"
GameWorld class that manages the game grid and all objects.
Handles object placement, collision detection, and world queries.
"

Object subclass: #GameWorld
    instanceVariableNames: 'width height objects hunter'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Core'

"Instance creation"
GameWorld class >> width: w height: h
    "Create a new game world with the given dimensions"
    ^ self new width: w height: h

"Initialization"
GameWorld >> initialize
    "Initialize the game world"
    super initialize.
    objects := OrderedCollection new.
    width := 10.
    height := 10

GameWorld >> width: w height: h
    "Set the world dimensions"
    width := w.
    height := h

"Accessing"
GameWorld >> width
    "Return the world width"
    ^ width

GameWorld >> height
    "Return the world height"
    ^ height

GameWorld >> objects
    "Return all objects in the world"
    ^ objects

GameWorld >> player
    "Return the hunter object"
    ^ hunter

"Object management"
GameWorld >> addObject: anObject
    "Add an object to the world"
    objects add: anObject.
    anObject world: self.
    anObject isPlayer ifTrue: [hunter := anObject]

GameWorld >> removeObject: anObject
    "Remove an object from the world"
    objects remove: anObject ifAbsent: []

GameWorld >> objectsAt: aPosition
    "Return all objects at the given position"
    ^ objects select: [:obj | obj position = aPosition]

GameWorld >> objectsAt: aPosition do: aBlock
    "Execute a block for each object at the given position"
    (self objectsAt: aPosition) do: aBlock

"Collision detection"
GameWorld >> isEmptyAt: aPosition for: requestingObject
    "Check if a position is empty (no movement-blocking objects)"
    ^ (self objectsAt: aPosition) allSatisfy: [:obj |
        (obj = requestingObject) or: [obj blocksMovement not]]

GameWorld >> hasVisionBlockingObjectAt: aPosition
    "Check if there's a vision-blocking object at the position"
    ^ (self objectsAt: aPosition) anySatisfy: [:obj | obj blocksVision]

"World setup"
GameWorld >> setupSimpleWorld
    "Create a simple world with some obstacles and deer"
    
    "Add some trees"
    self addObject: (Tree at: (Position x: 3 y: 2) inWorld: self).
    self addObject: (Tree at: (Position x: 7 y: 4) inWorld: self).
    self addObject: (Tree at: (Position x: 2 y: 6) inWorld: self).
    
    "Add some rocks"
    self addObject: (Rock at: (Position x: 5 y: 3) inWorld: self).
    self addObject: (Rock at: (Position x: 8 y: 7) inWorld: self).
    
    "Add some bushes"
    self addObject: (Bush at: (Position x: 4 y: 5) inWorld: self).
    self addObject: (Bush at: (Position x: 6 y: 8) inWorld: self).
    
    "Add deer"
    self addObject: (Deer at: (Position x: 3 y: 4) inWorld: self).
    self addObject: (Deer at: (Position x: 7 y: 2) inWorld: self).
    self addObject: (Deer at: (Position x: 9 y: 6) inWorld: self).
    self addObject: (Deer at: (Position x: 2 y: 8) inWorld: self).
    
    "Add hunter"
    self addObject: (Hunter at: (Position x: 5 y: 5) inWorld: self)

"Queries"
GameWorld >> deer
    "Return all deer in the world"
    ^ objects select: [:obj | obj isDeer]

GameWorld >> photographedDeer
    "Return all photographed deer"
    ^ self deer select: [:deer | deer isPhotographed]

GameWorld >> totalDeer
    "Return the total number of deer"
    ^ self deer size

GameWorld >> photographedDeerCount
    "Return the number of photographed deer"
    ^ self photographedDeer size

"Update"
GameWorld >> update
    "Update all objects in the world"
    objects do: [:obj | obj update]