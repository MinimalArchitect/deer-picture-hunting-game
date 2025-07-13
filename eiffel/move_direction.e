note
	description: "Summary description for {MOVE_DIRECTION}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

expanded class
	MOVE_DIRECTION

feature
	north, south, east, west: INTEGER is unique;

feature
	to_string(a_move_direction: INTEGER): STRING
		require
			valid_move_direction: is_move_direction(a_move_direction)
		do
			inspect a_move_direction
			when north then
				Result := "NORTH"
			when south then
				Result := "SOUTH"
			when west then
				Result := "WEST"
			when east then
				Result := "EAST"
			else
				Result := ""
			end
		end

feature
	is_move_direction(a_move_direction: INTEGER): BOOLEAN
		do
			Result := FALSE
			Result := Result or (a_move_direction = north)
			Result := Result or (a_move_direction = south)
			Result := Result or (a_move_direction = west)
			Result := Result or (a_move_direction = east)
		end
end
