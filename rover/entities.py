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


Location = namedtuple('Location', ('x', 'y'))
Grid = namedtuple('Grid', ('length', 'width'))
Rover = namedtuple('Rover', ('grid', 'location', 'direction'))
