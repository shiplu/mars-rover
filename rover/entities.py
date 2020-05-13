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
    STOP = "stopped"
    ERROR = "error"


Location = namedtuple("Location", ("x", "y"))


class SlottedBase:
    __slots__ = ()

    def __eq__(self, other):
        return all(
            getattr(self, slot) == getattr(other, slot) for slot in self.__slots__
        )

    def __repr__(self, other):
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

    def is_free(self, location):
        for rover in self.rovers:
            if rover.location == location:
                return False
        else:
            return True


class Rover(SlottedBase):
    __slots__ = ("grid", "location", "direction", "state")

    def __init__(self, grid, location, direction, state=None):
        if grid.is_free(location):
            self.location = location
            self.direction = direction
            self.grid = grid
            self.grid.add(self)
            self.state = state or RoverState.OPERATIONAL
        else:
            self.grid = None
            self.location = location
            self.direction = direction
            self.state = RoverState.ERROR

    def __hash__(self):
        return id(self)

    def move(self, *movements):
        pass
