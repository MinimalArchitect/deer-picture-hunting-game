"
Obstacle classes for trees, rocks, and bushes.
These objects block movement and/or vision.
"

GameObject subclass: #Obstacle
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

"Instance creation"
Obstacle class >> at: aPosition inWorld: aGameWorld
    "Create a new obstacle at the given position"
    ^ super at: aPosition inWorld: aGameWorld

"Testing"
Obstacle >> isObstacle
    "Return true - this is an obstacle"
    ^ true

Obstacle >> blocksMovement
    "Most obstacles block movement"
    ^ true

Obstacle >> blocksVision
    "Default - obstacles don't block vision"
    ^ false

"Tree - blocks both movement and vision"
Obstacle subclass: #Tree
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

Tree >> symbol
    "Display symbol for tree"
    ^ $T

Tree >> blocksVision
    "Trees block vision"
    ^ true

"Rock - blocks both movement and vision"
Obstacle subclass: #Rock
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

Rock >> symbol
    "Display symbol for rock"
    ^ $R

Rock >> blocksVision
    "Rocks block vision"
    ^ true

"Bush - allows movement but blocks vision"
Obstacle subclass: #Bush
    instanceVariableNames: ''
    classVariableNames: ''
    poolDictionaries: ''
    category: 'DeerHuntingGame-Objects'

Bush >> symbol
    "Display symbol for bush"
    ^ $B

Bush >> blocksMovement
    "Bushes don't block movement"
    ^ false

Bush >> blocksVision
    "Bushes block vision"
    ^ true