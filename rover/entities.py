from enum import Enum
from collections import namedtuple


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4

    # Aliases for above names. Just for the convenience
    N = 1
    E = 2
    S = 3
    W = 4


class Movement(Enum):
    MOVE = 10
    LEFT = 11
    RIGHT = 12

    # Aliases for above names. Just for the convenience
    M = 10
    L = 11
    R = 12


class RoverState(Enum):
    OPERATIONAL = "operational"
    STOPPED = "stopped"
    ERROR = "error"


Location = namedtuple("Location", ("x", "y"))


class Grid:
    __slots__ = ("length", "width", "rovers", "locations")

    def __init__(self, length, width):
        self.length = length
        self.width = width
        self.rovers = []
        self.locations = set()

    def __eq__(self, other):
        return self.length == other.length and self.width == other.width

    def __repr__(self):
        return "{}({!r}, {!r})".format(self.__class__.__name__, self.length, self.width)

    def add(self, rover):
        self.rovers.append(rover)
        self.fill(rover.location)

    def fill(self, location):
        self.locations.add(location)

    def free(self, location):
        self.locations.discard(location)

    def is_inside(self, location):
        return 0 < location.x <= self.length and 0 < location.y <= self.width

    def is_free(self, location):
        return location not in self.locations
        for rover in self.rovers:
            if rover.location == location:
                return False
        else:
            return True


class Rover:
    __slots__ = ("grid", "_location", "direction", "state")

    direction_map = {
        Movement.RIGHT: {
            Direction.NORTH: Direction.EAST,
            Direction.EAST: Direction.SOUTH,
            Direction.SOUTH: Direction.WEST,
            Direction.WEST: Direction.NORTH,
        },
        Movement.LEFT: {
            Direction.NORTH: Direction.WEST,
            Direction.WEST: Direction.SOUTH,
            Direction.SOUTH: Direction.EAST,
            Direction.EAST: Direction.NORTH,
        },
    }
    movement_map = {
        Direction.NORTH: (0, 1),
        Direction.EAST: (1, 0),
        Direction.SOUTH: (0, -1),
        Direction.WEST: (-1, 0),
    }

    def __init__(self, grid, location, direction, state=None):
        self.grid = None
        self.state = state or RoverState.OPERATIONAL
        self.direction = direction
        self.location = location

        if grid.is_free(location):
            self.grid = grid
            self.grid.add(self)
        else:
            self.state = RoverState.ERROR

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if self.grid is not None:
            self.grid.free(self._location)

        self._location = value

        if self.grid is not None:
            self.grid.fill(self._location)

    def __eq__(self, other):
        return (
            self.location == other.location
            and self.direction == other.direction
            and self.state == other.state
        )

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            self.__class__.__name__, self.location, self.direction, self.state
        )

    def __hash__(self):
        return id(self)

    def move(self, *movements):
        if self.state != RoverState.OPERATIONAL:
            return False

        for movement in movements:
            if movement in (Movement.RIGHT, Movement.LEFT):
                self.direction = self.direction_map[movement][self.direction]
                continue
            deltaX, deltaY = self.movement_map[self.direction]
            new_location = Location(self.location.x + deltaX, self.location.y + deltaY)
            if not (
                self.grid.is_inside(new_location) and self.grid.is_free(new_location)
            ):
                self.state = RoverState.STOPPED
                return False
            self.location = new_location

        return True
