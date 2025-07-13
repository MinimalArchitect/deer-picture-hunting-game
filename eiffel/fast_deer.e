-- FastDeer class with a stricter (but DbC-compliant) condition
class
    FAST_DEER

inherit
    DEER
        redefine can_be_photographed_by end

create make

feature
    can_be_photographed_by (player: PLAYER): BOOLEAN
            -- Only photographable if within 3-tile distance
        local
            dx, dy: INTEGER
            delta: DIRECTION
        do
        	delta := player.position - position
        	Result := delta.distance <= 3
        end

end

