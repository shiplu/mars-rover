from rover.entities import Direction
from rover.entities import Movement
from rover.entities import Grid
from rover.entities import Location
from rover.entities import Rover


class BaseParser:
    def __init__(self, data):
        self._parse(data)

    def _parse(self, data):
        raise NotImplementedError()


class GridParser(BaseParser):
    def _parse(self, data):
        length, width = tuple(map(int, data.split(" ")))
        self.grid = Grid(length, width)


class PositionParser(BaseParser):
    def _parse(self, data):
        segments = data.split(" ")
        self.location = Location(int(segments[0]), int(segments[1]))
        self.direction = Direction[segments[2]]


class MoveSequenceParser(BaseParser):
    def _parse(self, data):
        self.moves = [Movement[move] for move in data]


class InputParser(BaseParser):
    def _parse(self, data):
        lines = data.strip().splitlines()
        self.grid = GridParser(lines[0]).grid
        self.rovers_moves = []
        for position_index in list(range(1, len(lines), 2)):

            parsed_position = PositionParser(lines[position_index])
            rover = Rover(
                self.grid, parsed_position.location, parsed_position.direction
            )

            movement_sequences = MoveSequenceParser(lines[position_index + 1])
            moves = movement_sequences.moves

            self.rovers_moves.append((rover, moves))
