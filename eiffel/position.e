note
	description: "Summary description for {POSITION}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

class
	POSITION

create
	make

feature -- Initialize
	make (a_x, a_y: INTEGER)
		require
			valid_x: a_x >= 1 and a_x <= constants.map_width
			valid_y: a_y >= 1 and a_y <= constants.map_height
		do
			x := a_x
			y := a_y
		end

feature
	plus alias "+" (direction: DIRECTION): POSITION
		local
			position: POSITION
		do
			create position.make(x + direction.x, y + direction.y)
			Result := position
		end

feature
	subtract alias "-" (other: POSITION): DIRECTION
		local
			direction: DIRECTION
		do
			create direction.make(x - other.x, y - other.y)
			Result := direction
		end

feature {NONE}
	set_x(a_x: INTEGER)
		do
			x := a_x
		end

	set_y(a_y: INTEGER)
		do
			y := a_y
		end

feature
	is_position_within_bounds: BOOLEAN
		do
			Result := TRUE
			Result := Result and (x >= 1 and x <= constants.map_width)
			Result := Result and (y >= 1 and y <= constants.map_height)
		end

feature -- State
	x: INTEGER
	y: INTEGER
	constants: CONSTANTS

end
