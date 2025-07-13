note
	description: "Summary description for {GAME_OBJECT}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

class
	GAME_OBJECT

create
	make

feature
    make (a_position: Position; a_dir: INTEGER)
        require
            valid_position: a_position /= Void and a_position.is_position_within_bounds
            valid_move_direction: move_direction.is_move_direction(a_dir)
        do
            position := a_position
            direction := a_dir
        end

feature
    set_position (a_position: POSITION)
        require
            valid_position: a_position /= Void and a_position.is_position_within_bounds
        do
            position := a_position
        end

feature
    set_direction (a_dir: INTEGER)
        require
        	valid_move_direction: move_direction.is_move_direction(a_dir)
        do
            direction := a_dir
        end

feature -- State
    position: POSITION
    direction: INTEGER
    constants: CONSTANTS
    move_direction: MOVE_DIRECTION
end
