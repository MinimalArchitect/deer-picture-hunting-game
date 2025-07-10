"
Deer class representing the animals to be photographed.
Implements AI behavior to flee from the hunter.
"

GameObject subclass: #Deer
    instanceVariableNames: 'isPhotographed alertLevel'
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

"Instance creation"
Deer class >> at: aPosition inWorld: aGameWorld
    "Create a new deer at the given position"
    ^ super at: aPosition inWorld: aGameWorld

"Initialization"
Deer >> initialize
    "Initialize the deer"
    super initialize.
    isPhotographed := false.
    alertLevel := 0

"Accessing"
Deer >> isPhotographed
    "Return true if this deer has been photographed"
    ^ isPhotographed

Deer >> markAsPhotographed
    "Mark this deer as photographed"
    isPhotographed := true

Deer >> alertLevel
    "Return the current alert level"
    ^ alertLevel

"AI Behavior"
Deer >> update
    "Update the deer's behavior"
    | hunter distance |
    hunter := world player.
    distance := position distanceTo: hunter position.
    
    distance < 4 ifTrue: [
        alertLevel := alertLevel + 2.
        alertLevel := alertLevel min: 10
    ] ifFalse: [
        alertLevel := alertLevel - 1.
        alertLevel := alertLevel max: 0
    ].
    
    alertLevel > 5 ifTrue: [
        self fleeFromPlayer
    ] ifFalse: [
        self moveRandomly
    ]

Deer >> updateAdvanced
    "Advanced AI with line-of-sight awareness"
    | hunter distance |
    hunter := world player.
    distance := position distanceTo: hunter position.
    
    (hunter canSeePosition: position) ifTrue: [
        alertLevel := alertLevel + 3.
        alertLevel := alertLevel min: 10
    ] ifFalse: [
        distance < 3 ifTrue: [
            alertLevel := alertLevel + 1
        ] ifFalse: [
            alertLevel := alertLevel - 1.
            alertLevel := alertLevel max: 0
        ]
    ].
    
    alertLevel > 6 ifTrue: [
        self fleeFromPlayerSmart
    ] ifFalse: [
        alertLevel > 3 ifTrue: [
            self moveCarefully  
        ] ifFalse: [
            self moveRandomly
        ]
    ]

Deer >> fleeFromPlayer
    "Move away from the hunter"
    | hunter hunterPos bestDirection bestDistance |
    hunter := world player.
    hunterPos := hunter position.
    bestDirection := nil.
    bestDistance := 0.
    
    #(north south east west) do: [:dir |
        | newPos newDistance |
        newPos := position moveInDirection: dir.
        (self canMoveTo: newPos) ifTrue: [
            newDistance := newPos distanceTo: hunterPos.
            newDistance > bestDistance ifTrue: [
                bestDistance := newDistance.
                bestDirection := dir
            ]
        ]
    ].
    
    bestDirection ifNotNil: [
        self moveTo: (position moveInDirection: bestDirection)
    ]

Deer >> fleeFromPlayerSmart
    "Smart flee behavior"
    | hunter hunterPos bestDirection bestDistance directions |
    hunter := world player.
    hunterPos := hunter position.
    bestDirection := nil.
    bestDistance := 0.
    directions := #(north south east west).
    
    directions do: [:dir |
        | newPos newDistance |
        newPos := position moveInDirection: dir.
        (self canMoveTo: newPos) ifTrue: [
            newDistance := newPos distanceTo: hunterPos.
            newDistance > bestDistance ifTrue: [
                bestDistance := newDistance.
                bestDirection := dir
            ]
        ]
    ].
    
    bestDirection ifNil: [
        directions do: [:dir |
            | newPos |
            newPos := position moveInDirection: dir.
            (self canMoveTo: newPos) ifTrue: [
                bestDirection := dir.
                ^ self moveTo: newPos
            ]
        ]
    ] ifNotNil: [
        self moveTo: (position moveInDirection: bestDirection)
    ]

Deer >> moveRandomly
    "Move in a random direction"
    | directions randomDirection |
    (Random new next < 0.25) ifFalse: [^ self].
    
    directions := #(north south east west) asOrderedCollection.
    [directions notEmpty] whileTrue: [
        randomDirection := directions removeAt: (Random new nextInt: directions size).
        (self canMoveTo: (position moveInDirection: randomDirection)) ifTrue: [
            ^ self moveTo: (position moveInDirection: randomDirection)
        ]
    ]

Deer >> moveCarefully
    "Careful movement when alert"
    | directions randomDirection attempts |
    (Random new next < 0.15) ifFalse: [^ self].
    
    directions := #(north south east west) asOrderedCollection.
    attempts := 0.
    
    [directions notEmpty and: [attempts < 3]] whileTrue: [
        attempts := attempts + 1.
        randomDirection := directions removeAt: (Random new nextInt: directions size).
        (self canMoveTo: (position moveInDirection: randomDirection)) ifTrue: [
            ^ self moveTo: (position moveInDirection: randomDirection)
        ]
    ]

"Display"
Deer >> symbol
    "Return the display symbol for the deer"
    ^ isPhotographed ifTrue: [$X] ifFalse: [$D]

"Testing"
Deer >> isDeer
    "Return true - this is a deer"
    ^ true