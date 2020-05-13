from unittest import TestCase

from rover.parser import GridParser
from rover.parser import PositionParser
from rover.parser import MoveSequenceParser
from rover.parser import InputParser
from rover.entities import Direction
from rover.entities import Movement
from rover.entities import Grid
from rover.entities import Location
from rover.entities import Rover


class TestGridParser(TestCase):
    def test_basic(self):
        parsed = GridParser("3 4")
        self.assertEqual(parsed.grid, Grid(3, 4))


class TestPositionParser(TestCase):
    def test_basic(self):
        parsed = PositionParser("1 3 N")
        self.assertEqual(parsed.location, Location(1, 3))
        self.assertEqual(parsed.direction, Direction.N)


class TestMoveSequenceParser(TestCase):
    def test_basic(self):
        parsed_move_sequence = MoveSequenceParser("LMRM")
        self.assertEqual(parsed_move_sequence.moves, [Movement.L, Movement.M, Movement.R, Movement.M])


class TestInputParser(TestCase):
    def test_basic(self):
        parsed_input = InputParser("4 5\n1 2 N\nLML\n3 3 E\nMMR")
        self.assertEqual(parsed_input.grid, Grid(4, 5))
        self.assertEqual(len(parsed_input.rovers_moves), 2)
        self.assertEqual(parsed_input.rovers_moves[0][0],
                         Rover(Grid(4, 5), Location(1, 2), Direction.N))
        self.assertEqual(parsed_input.rovers_moves[0][1],
                         [Movement.L, Movement.M, Movement.L])
        self.assertEqual(parsed_input.rovers_moves[1][0],
                         Rover(Grid(4, 5), Location(3, 3), Direction.E))
        self.assertEqual(parsed_input.rovers_moves[1][1],
                         [Movement.M, Movement.M, Movement.R])
