from unittest import TestCase

from rover.entities import Direction
from rover.entities import Movement
from rover.entities import Grid
from rover.entities import Location
from rover.entities import Rover
from rover.entities import RoverState


class TestRover(TestCase):
    def assertRover(self, rover, grid=None, location=None, direction=None, state=None):
        if grid is not None:
            self.assertEqual(rover.grid, grid)
        if location is not None:
            self.assertEqual(rover.location, location)
        if direction is not None:
            self.assertEqual(rover.direction, direction)
        if state is not None:
            self.assertEqual(rover.state, state)

    def test_hashable(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(1, 1), Direction.N)
        r2 = Rover(g, Location(2, 2), Direction.N)
        r3 = Rover(g, Location(3, 3), Direction.N)
        rover_set = {r1, r2}
        self.assertIn(r1, rover_set)
        self.assertIn(r2, rover_set)
        self.assertNotIn(r3, rover_set)

        rover_set.add(r3)
        self.assertIn(r3, rover_set)

        self.assertEqual(rover_set, {r2, r3, r1})

    def test_initial_collision(self):
        g = Grid(2, 2)
        r1 = Rover(g, Location(1, 1), Direction.N)
        r2 = Rover(g, Location(1, 1), Direction.E)
        self.assertEqual(r1.state, RoverState.OPERATIONAL)
        self.assertEqual(r2.state, RoverState.ERROR)

    def test_move_north(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(2, 2), Direction.N)
        self.assertTrue(r1.move(Movement.M))
        self.assertRover(r1, g, Location(2, 3), Direction.N)

    def test_move_east(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(2, 2), Direction.E)
        self.assertTrue(r1.move(Movement.M))
        self.assertRover(r1, g, Location(3, 2), Direction.E)

    def test_move_south(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(2, 2), Direction.S)
        self.assertTrue(r1.move(Movement.M))
        self.assertRover(r1, g, Location(2, 1), Direction.S)

    def test_move_west(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(2, 2), Direction.W)
        self.assertTrue(r1.move(Movement.M))
        self.assertRover(r1, g, Location(1, 2), Direction.W)

    def test_move(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(1, 1), Direction.N)
        r1.move(Movement.M, Movement.R, Movement.M, Movement.M)
        self.assertRover(r1, g, Location(3, 2), Direction.E, RoverState.OPERATIONAL)

    def test_move_collision(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(1, 1), Direction.N)
        r2 = Rover(g, Location(2, 2), Direction.S)
        self.assertFalse(r1.move(Movement.M, Movement.R, Movement.M, Movement.M))
        self.assertRover(r1, g, Location(1, 2), Direction.E, RoverState.STOPPED)
        self.assertEqual(r2.state, RoverState.OPERATIONAL)

    def test_move_border_collision(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(1, 1), Direction.N)
        self.assertFalse(r1.move(Movement.M, Movement.M, Movement.M))
        self.assertRover(r1, g, Location(1, 3), Direction.N, RoverState.STOPPED)

    def test_disabled_movement(self):
        g = Grid(3, 3)
        r1 = Rover(g, Location(2, 2), Direction.N, RoverState.STOPPED)
        self.assertFalse(r1.move(Movement.M))
        self.assertEqual(r1.location, Location(2, 2))
