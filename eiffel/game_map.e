note
	description: "Summary description for {GAME_MAP}."
	author: ""
	date: "$Date$"
	revision: "$Revision$"

class
	GAME_MAP

create
	make

feature -- Initialization
	make
		do
            create map.make_filled(tile.empty, constants.map_width,constants.map_height)
            map.put(tile.tree, 3, 3)
            map.put(tile.rock, 2, 5)
            map.put(tile.bush, 5, 7)
            map.put(tile.tree, 8, 1)
            map.put(tile.tree, 4, 7)
		end

feature
	get_tile(a_position: Position): CHARACTER
		require
			valid_position: a_position /= Void and a_position.is_position_within_bounds
		do
			Result := map.item(a_position.y, a_position.x)
		end

feature {NONE} -- state
    map: ARRAY2[CHARACTER]
    constants: CONSTANTS
    tile: TILE
end
