from rover.entities import Direction
from rover.entities import Movement


class BaseParser:
    def __init__(self, line):
        self._parse(line)

    def _parse(self, line):
        raise NotImplementedError()


class GridParser(BaseParser):
    def _parse(self, line):
        self.length, self.width = tuple(map(int, line.split(' ')))


class PositionParser(BaseParser):

    def _parse(self, line):
        segments = line.split(' ')
        self.x, self.y = int(segments[0]), int(segments[1])
        self.direction = Direction[segments[2]]


class MoveSequenceParser(BaseParser):

    def _parse(self, line):
        self.moves = [Movement[move] for move in line]
