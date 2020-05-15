# coding:utf-8

"""Command line interface for mars rover control center"""

import argparse

from rover.parser import InputParser
from rover.entities import Direction
from rover.entities import RoverState


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "input", type=argparse.FileType(), help="input file contains commands"
    )
    parser.add_argument(
        "-f", "--format", choices=["text", "grid"], help="output format", default="text"
    )
    parser.add_argument(
        "-s", "--steps", help="shows all steps", action="store_true", default=False
    )
    return parser.parse_args()


class Format:

    direction_map = {
        Direction.N: "↑",
        Direction.S: "↓",
        Direction.E: "→",
        Direction.W: "←",
    }
    state_map = {
        RoverState.OPERATIONAL: "♥",
        RoverState.STOPPED: "Ø",
        RoverState.ERROR: "!",
    }

    @classmethod
    def grid(cls, grid):
        # Create empty grid
        rows = []
        for _ in range(grid.width):
            row = [""] * grid.length
            rows.append(row)

        # set the rovers
        for rover_index, rover in enumerate(grid.rovers, 1):
            text = "{}{}{}".format(
                rover_index,
                cls.direction_map[rover.direction],
                cls.state_map[rover.state],
            )
            rows[-rover.location.y][rover.location.x - 1] = text

        # format
        output = ""
        for row_num, row in enumerate(rows):
            output += "{:3}|{}|\n".format(
                grid.width - row_num,
                "|".join(["\033[4m{:^3}\033[0m".format(cell) for cell in row]),
            )
        else:
            output += "{:3} {}\n".format(
                "", " ".join(["{:3}".format(num + 1) for num in range(grid.length)])
            )
        return output

    def text(grid):
        lines = []
        for rover in grid.rovers:
            lines.append(
                "{} {} {} {}".format(
                    rover.location.x,
                    rover.location.y,
                    rover.direction.name[:1],
                    rover.state.name,
                )
            )
        return "\n".join(lines)


def main():
    args = parse_cli_arguments()
    data = args.input.read()
    format_func = Format.grid if args.format == "grid" else Format.text
    parsed_input = InputParser(data)

    if args.steps:
        print(format_func(parsed_input.grid))

    for rover_id, (rover, moves) in enumerate(parsed_input.rovers_moves, 1):
        for move in moves:
            success = rover.move(move)
            if args.steps:
                print(format_func(parsed_input.grid))
            if not success:
                break

    if not args.steps:
        print(format_func(parsed_input.grid))


if __name__ == "__main__":
    main()
