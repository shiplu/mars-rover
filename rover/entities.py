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


Location = namedtuple("Location", ('x', 'y'))


class SlottedBase:
    __slots__ = ()

    def __eq__(self, other):
        return all(
            getattr(self, slot) == getattr(other, slot) for slot in self.__slots__
        )

    def __repr__(self):
        args = ", ".join("{!r}".format(getattr(self, slot)) for slot in self.__slots__)
        return "{}({})".format(self.__class__.__name__, args)


class Grid(SlottedBase):
    __slots__ = ("length", "width", "rovers")

    def __init__(self, length, width, rovers=None):
        self.length = length
        self.width = width
        self.rovers = rovers or set([])

    def add(self, rover):
        self.rovers.add(rover)
        rover.grid = self

    def is_inside(self, location):
        return location.x <= self.length and location.y <= self.width

    def is_free(self, location):
        for rover in self.rovers:
            if rover.location == location:
                return False
        else:
            return True


class Rover(SlottedBase):
    __slots__ = ("grid", "location", "direction", "state")

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
        self.location = location
        self.direction = direction
        self.state = state or RoverState.OPERATIONAL
        self.grid = None

        if grid.is_free(location):
            self.grid = grid
            self.grid.add(self)
        else:
            self.state = RoverState.ERROR

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
            if not (self.grid.is_inside(new_location) and self.grid.is_free(new_location)):
                self.state = RoverState.STOPPED
                return False
            self.location = new_location

        return True
