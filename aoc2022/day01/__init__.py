from pathlib import Path


def main(input_file: Path) -> None:
    max_buffers = [0, 0, 0]
    with open(input_file, 'r') as f:
        buffer = 0
        for line in f:
            line = line.strip()
            if line != '':
                buffer += int(line)
            else:
                for i in range(3):
                    if buffer > max_buffers[i]:
                        max_buffers.insert(i, buffer)
                        max_buffers.pop()
                        break
                buffer = 0

    print(sum(max_buffers))
