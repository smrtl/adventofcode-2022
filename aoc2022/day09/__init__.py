from pathlib import Path
from typing import Set

import numpy as np
import numpy.typing as npt


class Rope:
    MOVES = {
        'U': np.array([0, 1]),
        'D': np.array([0, -1]),
        'L': np.array([-1, 0]),
        'R': np.array([1, 0]),
    }

    def __init__(self, count_knots: int = 2) -> None:
        self.knots = [np.array([0, 0]) for _ in range(count_knots)]
        self.count_knots = count_knots
        self.tail_log: Set[str] = set()

    def move_head(self, direction: str, distance: int) -> None:
        move = self.MOVES[direction]
        for _ in range(distance):
            self.update_rope(move)

    def update_rope(self, move: npt.NDArray[np.int_]) -> None:
        # update head
        self.knots[0] += move

        # update knots
        for index in range(1, self.count_knots):
            head = self.knots[index - 1]
            knot = self.knots[index]

            dx = abs(head[0] - knot[0])
            dy = abs(head[1] - knot[1])

            if dx > 1 or dy > 1:
                sx = np.sign(head[0] - knot[0])
                sy = np.sign(head[1] - knot[1])

                knot[0] = head[0] - sx if dx > 1 else head[0]
                knot[1] = head[1] - sy if dy > 1 else head[1]

        self.tail_log.add(str(self.knots[-1]))


def main(input_file: 'Path') -> None:
    rope = Rope(10)
    with open(input_file, 'r') as f:
        for line in f:
            [direction, distance] = line.strip().split()
            rope.move_head(direction, int(distance))
    print(len(rope.tail_log))
