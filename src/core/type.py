class Direction:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __mul__(self, scalar: int) -> 'Direction':
        assert isinstance(scalar, int), f"Can only multiply by int, got {type(scalar).__name__}"
        return Direction(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: int) -> 'Direction':
        return self.__mul__(scalar)

    def __add__(self, direction: 'Direction') -> 'Direction':
        assert isinstance(direction, Direction), f"Can only add by Direction, got {type(direction).__name__}"
        return Direction(self.x * direction.x, self.y * direction.y)

    def __radd__(self, direction: 'Direction') -> 'Direction':
        return self.__add__(direction)

    def distance(self) -> int:
        return abs(self.x) + abs(self.y)


class Position:
    def __init__(self, x: int, y: int) -> None:
        self._x = x
        self._y = y

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, direction: 'Direction') -> 'Position':
        assert isinstance(direction, Direction), f"Can only add Direction, got {type(direction).__name__}"
        return Position(self.x + direction.x, self.y + direction.y)

    def __radd__(self, direction: 'Direction') -> 'Position':
        return self.__add__(direction)

    def __sub__(self, position: 'Position') -> 'Direction':
        assert isinstance(position, Position), f"Can only subtract by Position, got {type(position).__name__}"
        return Direction(self.x - position.x, self.y - position.y)

    def __eq__(self, position: 'Position') -> bool:
        assert isinstance(position, Position), f"Can only compare Position, got {type(position).__name__}"
        return self.x == position.x and self.y == position.y
