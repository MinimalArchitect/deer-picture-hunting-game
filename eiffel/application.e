-- Root class
class
    APPLICATION

create
    make

feature -- Initialization

    make
    	local
            game: GAME
        do
            create game.make
            game.run
        end
end
