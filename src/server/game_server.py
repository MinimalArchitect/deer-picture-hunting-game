import random
import time
import uuid
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any
from weakref import WeakKeyDictionary

import pygame
from PodSixNet.Channel import Channel
from PodSixNet.Server import Server
from pygame.time import Clock

from src.core.config import GameServerConfig
from src.core.enum import MoveDirection, Tile
from src.core.event import ClientEvent
from src.core.type import Position, Direction
from src.server.game_map import GameMap

class GameObject(ABC):
    def __init__(self, position: Position) -> None:
        self._position = position
        self._direction = MoveDirection.UP

    @abstractmethod
    def handle_events(self, events: list[ClientEvent], context: 'GameServerContext') -> None:
        pass

    @abstractmethod
    def update(self, dt: int, context: 'GameServerContext') -> None:
        pass

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def direction(self) -> MoveDirection:
        return self._direction


class Player(Channel, GameObject):
    def __init__(self, *args, **kwargs) -> None:
        self.player_id = uuid.uuid4()
        Channel.__init__(self, *args, **kwargs)
        GameObject.__init__(self, Position(0, 0))
        self.deer_photographed: set[Deer] = set()
        self.has_photographed_player = False

    def set_position(self, position: Position) -> None:
        self._position = position

    def Close(self) -> None:
        self._server.remove_player(self)

    def Network_move(self, data) -> None:
        print(data)
        move_direction: MoveDirection = MoveDirection(data['move_direction'].upper())
        self._server.context.events.append(ClientEvent(self.player_id, move_direction, False))

    def Network_take_picture(self, data) -> None:
        self._server.context.events.append(ClientEvent(self.player_id, None, True))

    def Network_select_level(self, data) -> None:
        # Are we allowed to change a level?
        if self._server.is_level_reset_allowed():
            self._server.start_game(data['level'])

    def handle_events(self, events: list[ClientEvent], context: 'GameServerContext') -> None:
        for event in events:
            if event.player_id != self.player_id:
                continue

            assert (event.move_direction is not None and event.take_picture is False) \
                   or (event.move_direction is None and event.take_picture is True)

            if event.take_picture:
                self.take_picture(context)
                self.Send({'action': 'picture_taken'})

            if event.move_direction is not None:
                if event.move_direction == MoveDirection.UP:
                    self.move(Direction(0, -1), MoveDirection.UP, context)
                if event.move_direction == MoveDirection.DOWN:
                    self.move(Direction(0, +1), MoveDirection.DOWN, context)
                if event.move_direction == MoveDirection.LEFT:
                    self.move(Direction(-1, 0), MoveDirection.LEFT, context)
                if event.move_direction == MoveDirection.RIGHT:
                    self.move(Direction(+1, 0), MoveDirection.RIGHT, context)

    def update(self, dt: int, context: 'GameServerContext') -> None:
        pass

    def move(self, direction: Direction, move_direction: MoveDirection, context: 'GameServerContext') -> None:
        new_position = self.position + direction
        self._direction = move_direction

        is_deer_at_new_position = context.is_deer_at_position(new_position)
        is_player_at_new_position = context.is_player_at_position(new_position)

        if 0 <= new_position.x < GameServerConfig.GRID_WIDTH \
                and 0 <= new_position.y < GameServerConfig.GRID_HEIGHT \
                and context.map.get_tile(new_position) not in [Tile.TREE, Tile.ROCK] \
                and not is_deer_at_new_position \
                and not is_player_at_new_position:
            self.position = new_position
            self.Send({'action': 'moved'})

    def take_picture(self, context: 'GameServerContext') -> None:
        picture_direction = Direction(0, 0)
        match self._direction:
            case MoveDirection.UP:
                picture_direction = Direction(0, -1)
            case MoveDirection.DOWN:
                picture_direction = Direction(0, +1)
            case MoveDirection.LEFT:
                picture_direction = Direction(-1, 0)
            case MoveDirection.RIGHT:
                picture_direction = Direction(+1, 0)

        for i in range(1, GameServerConfig.PHOTO_RANGE + 1):
            position_to_check = self.position + i * picture_direction

            # Stop if we hit a boundary
            if not (0 <= position_to_check.x < GameServerConfig.GRID_WIDTH and 0 <= position_to_check.y < GameServerConfig.GRID_HEIGHT):
                break

            # Stop if we hit a solid obstacle
            if context.map.get_tile(position_to_check) in [Tile.TREE, Tile.ROCK, Tile.BUSH]:
                break

            for player in context.players:
                if player.position == position_to_check:
                    self.has_photographed_player = True

            for deer in context.deer:
                if deer.position == position_to_check:
                    self.deer_photographed.add(deer)

    def reset(self):
        self.deer_photographed = set()
        self.has_photographed_player = False


class Deer(GameObject, ABC):
    def __init__(self, position: Position, smell_distance: int, visual_distance: int, alert_threshold: int) -> None:
        super().__init__(position)
        self.alert_level = 0
        self.smell_distance = smell_distance
        self.visual_distance = visual_distance
        self.alert_threshold = alert_threshold

    def handle_events(self, events: list[ClientEvent], context: 'GameServerContext') -> None:
        pass

    def update(self, dt: int, context: 'GameServerContext') -> None:
        nearest_player = self._get_nearest_player(context)
        player_in_direct_sight = self._get_any_player_in_direct_sight(context)

        if nearest_player is None and player_in_direct_sight is None:
            self.alert_level -= 1  # Calm down over time
            self.random_walk(context)
            return
        elif player_in_direct_sight is not None:
            self.alert_level += 4
        elif nearest_player is not None and (self.position - nearest_player.position).distance() < self.smell_distance:
            self.alert_level += 2
        else:
            self.alert_level -= 1  # Calm down over time

        # Limit alert Level to 5 seconds and cooldown period to 10 seconds
        self.alert_level = clamp(self.alert_level, 0, 10 * GameServerConfig.FRAME_RATE)
        if self.alert_level < self.alert_threshold:
            self.random_walk(context)
        else:
            self.flee_from(nearest_player.position, context)

    def random_walk(self, context: 'GameServerContext') -> None:
        if random.random() >= 0.25:
            return

        possible_moves = [
            Direction(0, -1),
            Direction(0, +1),
            Direction(-1, 0),
            Direction(+1, 0)
        ]
        random.shuffle(possible_moves)

        deer_list = context.deer.copy()
        deer_list.remove(self)

        self.move_with_possible_directions(possible_moves, context)

    def flee_from(self, nearest_player_position: Position, context: 'GameServerContext') -> None:
        def sign(value: int) -> int:
            if value < 0:
                return -1
            elif value > 0:
                return 1
            else:
                return random.choice([-1, 1])

        dx = sign(nearest_player_position.x - self.position.x)
        dy = sign(nearest_player_position.y - self.position.y)

        # Try to move in that direction
        possible_moves = [
            Direction(-dx, 0),  # Horizontal away
            Direction(0, -dy),  # Vertical away
            Direction(-dx, -dy),  # Diagonal away
            Direction(0, 0)  # Stay put
        ]
        self.move_with_possible_directions(possible_moves, context)

    def move_with_possible_directions(self, possible_moves, context):
        # Try each move until we find a valid one
        for move in possible_moves:
            new_position = self.position + move

            is_deer_at_new_position = context.is_deer_at_position(new_position)
            is_player_at_new_position = context.is_player_at_position(new_position)

            if 0 <= new_position.x < GameServerConfig.GRID_WIDTH \
                    and 0 <= new_position.y < GameServerConfig.GRID_HEIGHT \
                    and context.map.get_tile(new_position) not in [Tile.TREE, Tile.ROCK] \
                    and not is_deer_at_new_position \
                    and not is_player_at_new_position:
                self.position = new_position
                break

    def _get_any_player_in_direct_sight(self, context: 'GameServerContext') -> Player | None:
        direction = Direction(0, 0)
        match self._direction:
            case MoveDirection.UP:
                direction = Direction(0, -1)
            case MoveDirection.DOWN:
                direction = Direction(0, +1)
            case MoveDirection.LEFT:
                direction = Direction(-1, 0)
            case MoveDirection.RIGHT:
                direction = Direction(+1, 0)

        for i in range(1, self.visual_distance + 1):
            position_to_check = self.position + i * direction

            # Stop if we hit a boundary
            if not (0 <= position_to_check.x < GameServerConfig.GRID_WIDTH and 0 <= position_to_check.y < GameServerConfig.GRID_HEIGHT):
                break

            # Stop if we hit a solid obstacle
            if context.map.get_tile(position_to_check) in [Tile.TREE, Tile.ROCK, Tile.BUSH]:
                break

            for player in context.players:
                if player.position == position_to_check:
                    return player
        return None

    def _get_nearest_player(self, context: 'GameServerContext') -> Player | None:
        nearest_player: Player | None = None
        for player in context.players:
            if nearest_player is None:
                nearest_player = player
            else:
                distance_to_nearest_player = (self.position - nearest_player.position).distance()
                distance_to_current_player = (self.position - player.position).distance()

                if distance_to_current_player < distance_to_nearest_player:
                    nearest_player = player
        return nearest_player


class BlindDeer(Deer):
    def __init__(self, position: Position) -> None:
        super().__init__(position, 5, 7, 40)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def direction(self) -> MoveDirection:
        return self._direction


class MediumDeer(Deer):
    def __init__(self, position: Position) -> None:
        super().__init__(position, 6, 8, 40)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def direction(self) -> MoveDirection:
        return self._direction


class SuperDeer(Deer):
    def __init__(self, position: Position) -> None:
        super().__init__(position, 6, 8, 30)

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, value: Position) -> None:
        self._position = value

    @property
    def direction(self) -> MoveDirection:
        return self._direction


def clamp(n: int, lower: int, upper: int) -> int:
    return max(lower, min(n, upper))


class GameServerContext:
    def __init__(self) -> None:
        self._clock = pygame.time.Clock()

        self.level = 10
        self._map = GameMap(level=self.level)

        self._players: WeakKeyDictionary[Player, bool] = WeakKeyDictionary()
        self._deer = self._generate_deer_wave(level=self.level)

        self._events: list[ClientEvent] = []
        self._game_start_time = time.time()

    def _generate_deer_wave(self, level: int) -> list[Deer]:
        assert GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL
        total_deer = GameServerConfig.DEER_COUNT

        if level <= 5:
            num_blind = total_deer
            num_medium = 0
            num_super = 0
        elif level <= 13:
            num_medium = level - 5
            num_blind = total_deer - num_medium - 1
            num_super = 1
        else:
            num_super = level - 12
            num_medium = total_deer - num_super
            num_blind = 0

        deer_list: list[Deer] = []
        deer_list.extend([BlindDeer(self._map.get_empty_tile()) for _ in range(num_blind)])
        deer_list.extend([MediumDeer(self._map.get_empty_tile()) for _ in range(num_medium)])
        deer_list.extend([SuperDeer(self._map.get_empty_tile()) for _ in range(num_super)])

        return deer_list

    @property
    def clock(self) -> Clock:
        return self._clock

    @property
    def deer(self) -> list[Deer]:
        return self._deer

    @property
    def players(self) -> WeakKeyDictionary[Player, bool]:
        return self._players

    @property
    def events(self) -> list[ClientEvent]:
        return self._events

    @property
    def map(self) -> GameMap:
        return self._map

    def is_player_at_position(self, new_position: Position) -> bool:
        for player in self.players:
            if player.position == new_position:
                return True
        return False

    def is_deer_at_position(self, new_position: Position) -> bool:
        for deer in self.deer:
            if deer.position == new_position:
                return True
        return False

    def reset(self, level: int):
        assert GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL
        self.level = level
        self._map = GameMap(level=self.level)

        [player.reset() for player in self.players]
        [player.set_position(self.map.get_empty_tile()) for player in self.players]
        self._deer = self._generate_deer_wave(level=self.level)

        self._events: list[ClientEvent] = []

    @property
    def game_start_time(self):
        return self._game_start_time

    @game_start_time.setter
    def game_start_time(self, value):
        self._game_start_time = value


class GameServerState(StrEnum):
    LEVEL_SELECTION = 'LEVEL_SELECTION'
    PLAYING = 'PLAYING'
    FINISHED = 'FINISHED'


class GameServer(Server):
    channelClass = Player

    def __init__(self, config: GameServerConfig) -> None:
        super().__init__(localaddr=config.host)
        pygame.init()
        self.config: GameServerConfig = config
        self.context: GameServerContext = GameServerContext()
        print('Server Launched')
        self.passed_time = 0  # in ms
        self.state = GameServerState.LEVEL_SELECTION

    def Connected(self, player: Player, address: Any) -> None:
        if self.state != GameServerState.LEVEL_SELECTION:
            player.Close()
        position = self.context.map.get_empty_tile()
        player.set_position(position)
        self.add_player(player)

    def add_player(self, player) -> None:
        print(f'New Player {str(player.addr)}')
        self.context.players[player] = True
        print(f'players: {[player for player in self.context.players]}')

    def remove_player(self, player: Player) -> None:
        print(f'Removing Player {str(player.addr)}')
        del self.context.players[player]

    def send_to_all(self, data: dict[str, Any]) -> None:
        [player.Send(data) for player in self.context.players]

    def send_score(self):
        [player.Send({'action': 'score', 'score': len(player.deer_photographed) if not player.has_photographed_player else -1}) for player in self.context.players]

    def is_level_reset_allowed(self) -> bool:
        return self.state == GameServerState.LEVEL_SELECTION

    def start_game(self, level: int) -> None:
        assert GameServerConfig.MIN_LEVEL <= level <= GameServerConfig.MAX_LEVEL
        self.context.reset(level)
        self.state = GameServerState.PLAYING
        self.context.game_start_time = time.time()
        self.send_to_all({
            'action': 'game_started',
            'level': level,
        })

    def update(self, dt: int) -> None:
        ClientEvent.remove_duplicate_client_events(self.context.events)

        [player.handle_events(self.context.events, self.context) for player in self.context.players]
        [deer.handle_events(self.context.events, self.context) for deer in self.context.deer]

        [player.update(dt, self.context) for player in self.context.players]
        [deer.update(dt, self.context) for deer in self.context.deer]

        self.context.events.clear()

        self.send_to_all({
            'action': 'state_update',
            'message': {
                'players': [{'x': player.position.x, 'y': player.position.y, 'direction': player.direction.name} for player in self.context.players],
                'deer': [{'x': deer.position.x, 'y': deer.position.y, 'direction': deer.direction.name} for deer in self.context.deer],
                'time_left': self.context.game_start_time + GameServerConfig.GAME_DURATION - time.time()
            }
        })

    def run(self) -> None:
        while True:
            if self.state == GameServerState.LEVEL_SELECTION:
                self.Pump()
                time.sleep(0.001)
            if self.state == GameServerState.PLAYING:
                print(self.context.game_start_time + GameServerConfig.GAME_DURATION - time.time())
                self.Pump()
                self.update(self.passed_time)
                self.passed_time = self.context.clock.tick(GameServerConfig.FRAME_RATE)

                if time.time() >= self.context.game_start_time + GameServerConfig.GAME_DURATION:
                    self.state = GameServerState.FINISHED

            elif self.state == GameServerState.FINISHED:
                self.send_score()
                self.state = GameServerState.LEVEL_SELECTION
