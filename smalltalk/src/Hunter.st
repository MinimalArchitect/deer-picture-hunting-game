"
Hunter class representing the player character.
Handles movement, direction tracking, and photography.
"

GameObject subclass: #Hunter
    instanceVariableNames: 'direction score photosTaken'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

"Instance creation"
Hunter class >> at: aPosition inWorld: aGameWorld
    "Create a new hunter at the given position"
    ^ super at: aPosition inWorld: aGameWorld

"Initialization"
Hunter >> initialize
    "Initialize the hunter"
    super initialize.
    direction := #north.
    score := 0.
    photosTaken := 0

"Accessing"
Hunter >> direction
    "Return the current facing direction"
    ^ direction

Hunter >> direction: aDirection
    "Set the facing direction"
    direction := aDirection

Hunter >> score
    "Return the current score"
    ^ score

Hunter >> photosTaken
    "Return the number of photos taken"
    ^ photosTaken

"Movement"
Hunter >> moveNorth
    "Move north and face north"
    direction := #north.
    ^ self moveTo: (position north)

Hunter >> moveSouth
    "Move south and face south"
    direction := #south.
    ^ self moveTo: (position south)

Hunter >> moveEast
    "Move east and face east"
    direction := #east.
    ^ self moveTo: (position east)

Hunter >> moveWest
    "Move west and face west"
    direction := #west.
    ^ self moveTo: (position west)

Hunter >> moveInDirection: aDirection
    "Move in the specified direction"
    aDirection = #north ifTrue: [^ self moveNorth].
    aDirection = #south ifTrue: [^ self moveSouth].
    aDirection = #east ifTrue: [^ self moveEast].
    aDirection = #west ifTrue: [^ self moveWest].
    ^ false

Hunter >> moveInDirectionWithBounds: aDirection
    "Move in direction with bounds checking"
    | newPosition |
    newPosition := position moveInDirection: aDirection.
    
    (newPosition isValidInWorld: world) ifFalse: [
        ^ false
    ].
    
    direction := aDirection.
    ^ self moveTo: newPosition

"Photography"
Hunter >> takePhoto
    "Take a photo in the current direction"
    | visibleObjects deer |
    photosTaken := photosTaken + 1.
    visibleObjects := self getVisibleObjects.
    deer := visibleObjects select: [:obj | obj isDeer].
    deer do: [:each | 
        (each isPhotographed not) ifTrue: [
            each markAsPhotographed.
            score := score + 1.
            ^ each
        ]
    ].
    ^ nil

Hunter >> takePhotoAdvanced
    "Advanced photography with line-of-sight"
    | photographedDeer |
    photosTaken := photosTaken + 1.
    photographedDeer := OrderedCollection new.
    
    world deer do: [:deer |
        (self canSeePosition: deer position) ifTrue: [
            (deer isPhotographed not) ifTrue: [
                deer markAsPhotographed.
                score := score + 1.
                photographedDeer add: deer
            ]
        ]
    ].
    
    ^ photographedDeer

Hunter >> canSeePosition: targetPosition
    "Check if hunter can see target position"
    | currentPos |
    currentPos := position.
    
    1 to: 10 do: [:step |
        currentPos := currentPos moveInDirection: direction.
        
        (currentPos isValidInWorld: world) ifFalse: [^ false].
        currentPos = targetPosition ifTrue: [^ true].
        
        (world hasVisionBlockingObjectAt: currentPos) ifTrue: [^ false]
    ].
    ^ false

Hunter >> getVisibleObjects
    "Get all objects visible in the current direction"
    | currentPos objects maxRange |
    objects := OrderedCollection new.
    currentPos := position.
    maxRange := 10.
    
    1 to: maxRange do: [:distance |
        currentPos := currentPos moveInDirection: direction.
        (currentPos isValidInWorld: world) ifFalse: [^ objects].
        
        world objectsAt: currentPos do: [:obj |
            objects add: obj.
            obj blocksVision ifTrue: [^ objects]
        ]
    ].
    ^ objects

"Display"
Hunter >> symbol
    "Return the display symbol for the hunter"
    direction = #north ifTrue: [^ $↑].
    direction = #south ifTrue: [^ $↓].
    direction = #east ifTrue: [^ $→].
    direction = #west ifTrue: [^ $←].
    ^ $H

"Testing"
Hunter >> isPlayer
    "Return true - this is a player"
    ^ true