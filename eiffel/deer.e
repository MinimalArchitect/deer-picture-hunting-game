class
    DEER

inherit
	GAME_OBJECT

create
	make

feature
    can_be_photographed_by (p: PLAYER): BOOLEAN
            -- Determines whether player can photograph this deer
        do
            Result := True
        end

feature
	update(map: GAME_MAP; player: PLAYER)
		do

		end
end


