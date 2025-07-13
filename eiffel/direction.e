note
	description: "Summary description for {DIRECTION}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

class
	DIRECTION

create make

feature
	make(a_x, a_y: INTEGER)
	do
		x := a_x
		y := a_y
	end

feature
	plus alias "+" (other: DIRECTION): DIRECTION
		local
			direction: DIRECTION
		do
			create direction.make(x + other.x, y + other.y)
			Result := direction
		end
feature
	multiply alias "*" (scalar: INTEGER): DIRECTION
		local
			direction: DIRECTION
		do
			create direction.make(x * scalar, y * scalar)
			Result := direction
		end

feature
	distance: INTEGER
		do
			Result := x.abs + y.abs
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
	x: INTEGER
	y: INTEGER
end
