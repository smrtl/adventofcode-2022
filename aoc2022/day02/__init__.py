from pathlib import Path

LOOSE_SCORE = 0
DRAW_SCORE = 3
WIN_SCORE = 6

ROCK = 1
PAPER = 2
SCISSORS = 3

# imagine rock, paper, scissors are in an array like that:
#       [1, 2, 3]
# if the elf picks rock, the outcomes depending on the player choice is:
#       [D, W, L]
# ie. if the player picks rock (1) too, it's a draw, ...
# Now if the elf picks paper we have the following:
#       [L, D, W]
#
# This is how we compute the below offsets
WIN_OFFSET = 0
LOOSE_OFFSET = 1
DRAW_OFFSET = 2

moves = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS,
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS,
}

outcomes = {
    'X': {
        'offset': LOOSE_OFFSET,
        'score': LOOSE_SCORE
    },
    'Y': {
        'offset': DRAW_OFFSET,
        'score': DRAW_SCORE
    },
    'Z': {
        'offset': WIN_OFFSET,
        'score': WIN_SCORE
    },
}


def run_match(elf_move: str, player_move: str) -> int:
    player_value = moves[player_move]
    value = player_value - moves[elf_move]

    if value == 1 or value == -2:
        score = WIN_SCORE
    elif value == 0:
        score = DRAW_SCORE
    else:
        score = LOOSE_SCORE

    return player_value + score


def part1(input_file: Path) -> None:
    score = 0
    with open(input_file, 'r') as fd:
        for line in fd:
            [elf_move, player_move] = line.strip().split(' ')
            score += run_match(elf_move, player_move)
    print(score)


def solve_match(elf_move: str, result: str) -> int:
    outcome = outcomes[result]
    player_move = 1 + (outcome['offset'] + moves[elf_move]) % 3
    return player_move + outcome['score']


def part2(input_file: Path) -> None:
    score = 0
    with open(input_file, 'r') as fd:
        for line in fd:
            [elf_move, match_outcome] = line.strip().split(' ')
            score += solve_match(elf_move, match_outcome)
    print(score)


def main(input_file: Path) -> None:
    part2(input_file)
