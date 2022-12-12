from pathlib import Path
from collections import deque

MAX_ELEVATION = ord('z')


def find_path_to_end(world, start) -> int:
    width = len(world[0])
    height = len(world)
    queue = deque([[start]])
    visited = set([start])
    min_path_len = float('inf')

    while len(queue) > 0:
        path = queue.popleft()
        (x, y) = path[-1]
        elevation = ord(world[y][x])

        for target in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            if 0 <= target[0] < width and 0 <= target[1] < height:
                target_value = world[target[1]][target[0]]
                target_elevation = ord(target_value) if target_value != 'E' else MAX_ELEVATION

                if target_elevation <= elevation + 1 and target not in visited:
                    if target_value == 'E':
                        min_path_len = min(min_path_len, len(path))
                    else:
                        visited.add(target)
                        queue.append(path + [target])

    return min_path_len


def main(input_file: Path) -> None:
    world = []
    start = None
    with open(input_file, 'r') as fd:
        for row_index, line in enumerate(fd):
            start_index = line.find('S')
            if start_index >= 0:
                start = (start_index, row_index)
                line = line.replace('S', 'a')
            world.append(line.strip())

    if not start:
        raise ValueError('Start point not found')

    min_path_len = float('inf')
    for row_index, line in enumerate(world):
        for col_index, char in enumerate(line):
            if char == 'a':
                path_len = find_path_to_end(world, (col_index, row_index))
                min_path_len = min(min_path_len, path_len)

    print('Min path len', min_path_len)
