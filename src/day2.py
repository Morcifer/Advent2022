from typing import List, Optional, Tuple

from src.utilities import load_data


DAY = 2

ROCK = 1
PAPER = 2
SCISSORS = 3

TO_WIN = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK
}

TO_LOSE = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}

OPPONENT_CHOICES = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}

MY_CHOICES = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}


def parser(s: List[str]) -> Tuple[int, int]:
    return OPPONENT_CHOICES[s[0]], MY_CHOICES[s[1]]


EXPECTED_RESULTS = {
    "X": 0,
    "Y": 3,
    "Z": 6
}


def parser_2(s: List[str]) -> Tuple[int, int]:
    return OPPONENT_CHOICES[s[0]], EXPECTED_RESULTS[s[1]]


def determine_game_scores(data: List[Tuple[int, int]]) -> List[int]:
    results = []
    for opponent_choice, my_choice in data:
        if opponent_choice == my_choice:
            expected_result = 3  # draw
        elif TO_WIN[opponent_choice] == my_choice:
            expected_result = 6
        elif TO_LOSE[opponent_choice] == my_choice:
            expected_result = 0
        else:
            raise ValueError()

        results.append(expected_result + my_choice)

    return results


def part_1() -> int:
    data = load_data(DAY, parser, "data", is_test=False)
    return sum(determine_game_scores(data))


def determine_game_scores_2(data: List[Tuple[int, int]]) -> List[int]:
    results = []
    for opponent_choice, expected_result in data:
        if expected_result == 0:
            my_choice = TO_LOSE[opponent_choice]
        elif expected_result == 3:
            my_choice = opponent_choice
        elif expected_result == 6:
            my_choice = TO_WIN[opponent_choice]
        else:
            raise ValueError()

        results.append(expected_result + my_choice)
    return results


def part_2() -> int:
    data = load_data(DAY, parser_2, "data", is_test=False)
    return sum(determine_game_scores_2(data))


if __name__ == '__main__':
    print(f"Day {DAY} result 1: {part_1()}")
    print(f"Day {DAY} result 2: {part_2()}")
