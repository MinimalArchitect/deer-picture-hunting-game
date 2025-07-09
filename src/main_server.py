from src.core.config import GameServerConfig
from src.server.game_server import GameServer

if __name__ == "__main__":
    game_server_config = GameServerConfig()

    game_server = GameServer(game_server_config)
    game_server.run()
