"
GameObject - Abstract base class for all objects in the deer hunting game.
Provides common functionality for position management and world interaction.
"

Object subclass: #GameObject
    instanceVariableNames: 'position world'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

"Instance creation"
GameObject class >> at: aPosition inWorld: aGameWorld
    "Create a new game object at the given position"
    ^ self new position: aPosition; world: aGameWorld; yourself

"Initialization"
GameObject >> initialize
    "Initialize a new game object"
    super initialize.
    position := Position x: 1 y: 1

"Accessing"
GameObject >> position
    "Return the current position"
    ^ position

GameObject >> position: aPosition
    "Set the position"
    position := aPosition

GameObject >> world
    "Return the game world"
    ^ world

GameObject >> world: aGameWorld
    "Set the game world"
    world := aGameWorld

GameObject >> x
    "Return x coordinate"
    ^ position x

GameObject >> y
    "Return y coordinate"
    ^ position y

"Movement"
GameObject >> moveTo: newPosition
    "Move to a new position if valid"
    (self canMoveTo: newPosition) ifTrue: [
        position := newPosition.
        ^ true
    ].
    ^ false

GameObject >> canMoveTo: aPosition
    "Check if this object can move to the given position"
    ^ (aPosition isValidInWorld: world) and: [
        world isEmptyAt: aPosition for: self]

"Game symbols for display"
GameObject >> symbol
    "Return the symbol used to display this object (subclass responsibility)"
    self subclassResponsibility

"Update"
GameObject >> update
    "Update this object's state (subclass responsibility)"
    "Default implementation does nothing"

"Testing"
GameObject >> isPlayer
    "Return true if this is a player object"
    ^ false

GameObject >> isDeer
    "Return true if this is a deer object"
    ^ false

GameObject >> isObstacle
    "Return true if this is an obstacle"
    ^ false

GameObject >> blocksMovement
    "Return true if this object blocks movement"
    ^ false

GameObject >> blocksVision
    "Return true if this object blocks vision"
    ^ false

"Printing"
GameObject >> printOn: aStream
    "Print a readable representation"
    aStream nextPutAll: self class name; 
            nextPutAll: ' at '; 
            print: position