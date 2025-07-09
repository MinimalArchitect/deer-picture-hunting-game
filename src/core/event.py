from uuid import UUID

from src.core.enum import MoveDirection


class ClientEvent:
    def __init__(self, player_id: UUID, move_direction: MoveDirection | None, take_picture: bool) -> None:
        assert (move_direction is not None and take_picture is False) or (move_direction is None and take_picture is True)
        self._player_id = player_id
        self._move_direction = move_direction
        self._take_picture = take_picture

    @classmethod
    def remove_duplicate_client_events(cls, events: list['ClientEvent']) -> None:
        seen: set[UUID] = set()
        result = []
        for event in events:
            player = event.player_id
            if player not in seen:
                seen.add(player)
                result.append(event)

        events.clear()
        events.extend(result)

    @property
    def move_direction(self) -> MoveDirection | None:
        return self._move_direction

    @property
    def take_picture(self) -> bool:
        return self._take_picture

    @property
    def player_id(self) -> UUID:
        return self._player_id
