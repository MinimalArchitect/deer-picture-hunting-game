-- Game logic class
class
	GAME

create
	make

feature -- Initialization

	make
		local
			d: DEER
			fast_deer: FAST_DEER
			position: POSITION
		do
			create map.make

			deer_count := 3

			create deer_list.make(deer_count)
			create position.make(5, 7)
			create d.make(position, move_direction.north)
			deer_list.extend(d)
			create position.make(8, 2)
			create d.make(position, move_direction.north)
			deer_list.extend(d)
			create position.make(2, 6)
			create fast_deer.make(position, move_direction.north)
			deer_list.extend(fast_deer)

			create position.make(3, 7)
			create player.make(position, move_direction.south)

			photos_taken := 0

			create random_sequence.make
		ensure
			map_initialized: map /= Void
			player_initialized: player /= Void
			deer_initialized: deer_list.count = deer_count
			photo_count_zero: photos_taken = 0
		end

feature -- Game Loop

	run
		require
			initialized: map /= Void and player /= Void and deer_list /= Void
		local
			playing: BOOLEAN
			input: STRING
			new_x, new_y: INTEGER
			target_tile: CHARACTER
			new_position: POSITION
		do
			playing := True
			from until not playing loop
				-- update
				update

				-- render
				draw_map

				-- handle event
				io.put_string("%NFacing: " + move_direction.to_string(player.direction) + " | Photos taken: " + photos_taken.out + "/" + deer_count.out)
				io.put_string("%NUse WASD to move, F to photograph, Q to quit: ")
				io.read_line
				input := io.last_string.as_upper

				new_x := player.position.x
				new_y := player.position.y

				if input.same_string("W") and player.position.y > 1 then
					new_y := player.position.y - 1
					player.set_direction(move_direction.north)
				elseif input.same_string("S") and player.position.y < constants.map_height then
					new_y := player.position.y + 1
					player.set_direction(move_direction.south)
				elseif input.same_string("A") and player.position.x > 1 then
					new_x := player.position.x - 1
					player.set_direction (move_direction.west)
				elseif input.same_string("D") and player.position.x < constants.map_width then
					new_x := player.position.x + 1
					player.set_direction (move_direction.east)
				elseif input.same_string("F") then
					if photograph_deer then
						io.put_string("%NYou successfully photographed a deer!%N")
					else
						io.put_string("%NNo deer in sight!%N")
					end
				elseif input.same_string("Q") then
					playing := False
				end

				create new_position.make(new_x, new_y)
				target_tile := map.get_tile(new_position)
				if not deer_at(new_position) and then not (target_tile = tile.tree or target_tile = tile.rock or target_tile = tile.bush) then
					player.set_position(new_position)
				end

				if photos_taken = deer_count then
					io.put_string("%NAll deer photographed!%N")
					playing := False
				end
			end

			io.put_string("%NGame Over. Thanks for playing.%N")
		end

feature -- Update
	update
		require
			map_ready: map /= Void
			deer_list_ready: deer_list /= Void
			player_ready: player /= Void
		do
			across deer_list as deer loop
				deer.item.update(map, player)
			end
		end

feature -- Drawing

	draw_map
		require
			map_ready: map /= Void
		local
			y, x: INTEGER
			visible: BOOLEAN
			print_position: POSITION
		do
			io.put_string("%N%N%N================= MAP =================%N")
			from y := 1 until y > constants.map_height loop
				from x := 1 until x > constants.map_width loop
					visible := False
					if y = player.position.y and x = player.position.x then
						io.put_character(tile.player)
						visible := True
					else
						across deer_list as c loop
							if y = c.item.position.y and x = c.item.position.x then
								visible := True
								io.put_character(tile.deer)
							end
						end
					end
					if not visible then
						create print_position.make(x, y)
						io.put_character(map.get_tile(print_position))
					end
					io.put_character(' ')
					x := x + 1
				end
				io.put_new_line
				y := y + 1
			end
		end

feature -- Detection & Interaction

	photograph_deer: BOOLEAN
		require
			map_ready: map /= Void
			player_ready: player /= Void
			deer_list_ready: deer_list /= Void
		local
			scan_x, scan_y: INTEGER
			obstacle_found: BOOLEAN
			d: DEER
			scan_position: Position
		do
			from deer_list.start
			until deer_list.exhausted
			loop
				d := deer_list.item
				obstacle_found := False
				if d.can_be_photographed_by (player) then


					if equal(player.direction, move_direction.north) and player.position.x = d.position.x and player.position.y > d.position.y then
						from scan_y := player.position.y - 1 until scan_y < d.position.y or obstacle_found loop
							create scan_position.make(player.position.x, scan_y)
							if map.get_tile(scan_position) /= tile.empty and map.get_tile(scan_position) /= tile.deer then obstacle_found := True end
							scan_y := scan_y - 1
						end
						if not obstacle_found then
							photos_taken := photos_taken + 1
							Result := True
							deer_list.remove
						else
							deer_list.forth
						end
					elseif equal(player.direction, move_direction.south) and player.position.x = d.position.x and player.position.y < d.position.y then
						from scan_y := player.position.y + 1 until scan_y > d.position.y or obstacle_found loop
							create scan_position.make(player.position.x, scan_y)
							if map.get_tile(scan_position) /= tile.empty and map.get_tile(scan_position) /= tile.deer then obstacle_found := True end
							scan_y := scan_y + 1
						end
						if not obstacle_found then
							photos_taken := photos_taken + 1
							Result := True
							deer_list.remove
						else
							deer_list.forth
						end
					elseif equal(player.direction, move_direction.west) and player.position.y = d.position.y and player.position.x > d.position.x then
						from scan_x := player.position.x - 1 until scan_x < d.position.x or obstacle_found loop
							create scan_position.make(scan_x, player.position.y)
							if map.get_tile(scan_position) /= tile.empty and map.get_tile(scan_position) /= tile.deer then obstacle_found := True end
							scan_x := scan_x - 1
						end
						if not obstacle_found then
							photos_taken := photos_taken + 1
							Result := True
							deer_list.remove
						else
							deer_list.forth
						end
					elseif equal(player.direction, move_direction.east) and player.position.y = d.position.y and player.position.x < d.position.x then
						from scan_x := player.position.x + 1 until scan_x > d.position.x or obstacle_found loop
							create scan_position.make(scan_x, player.position.y)
							if map.get_tile(scan_position) /= tile.empty and map.get_tile(scan_position) /= tile.deer then obstacle_found := True end
							scan_x := scan_x + 1
						end
						if not obstacle_found then
							photos_taken := photos_taken + 1
							Result := True
							deer_list.remove
						else
							deer_list.forth
						end
					else
						deer_list.forth
					end
				else
					deer_list.forth
				end
			end

		ensure
			result_boolean: Result = True implies photos_taken > 0
		end

feature {NONE}
	deer_at (position: POSITION): BOOLEAN
		require
			position_valid: position /= Void and position.is_position_within_bounds
			deer_list_exists: deer_list /= Void
		do
			Result := False
			across deer_list as c loop
				if position.is_equal(c.item.position) then
					Result := True
				end
			end

		ensure
			result_true_if_match: Result implies across deer_list as c some c.item.position.is_equal(position) end
		end

feature {NONE}
	new_random: INTEGER
		-- Random integer
		-- Each call returns another random number.
	do
		random_sequence.forth
		Result := random_sequence.item
	end

feature -- State
	map: GAME_MAP
	player: PLAYER
	deer_count: INTEGER
	deer_list: ARRAYED_LIST[DEER]
	photos_taken: INTEGER
	constants : CONSTANTS
	random_sequence: RANDOM
	tile: TILE
	move_direction: MOVE_DIRECTION
end
