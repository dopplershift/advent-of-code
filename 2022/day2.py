import enum

class RPS(enum.IntEnum):
    Rock = 1
    Paper = 2
    Scissors = 3

source = {'A': RPS.Rock, 'B': RPS.Paper, 'C': RPS.Scissors}
choice = {'X': RPS.Rock, 'Y': RPS.Paper, 'Z': RPS.Scissors}


def score1(matchup):
    opp = source[matchup[0]]
    mine = choice[matchup[-1]]
    if opp == mine:
        outcome = 3
    elif opp - mine in (1, -2):
        outcome = 0
    else:
        outcome = 6
    return mine + outcome


def score2(matchup):
    opp = source[matchup[0]]
    res = matchup[-1]

    if res == 'X':  # Lose
        return (opp - 2) % 3 + 1
    elif res == 'Y':  # Draw
        return 3 + opp
    else: # 'Z' -> Win
        return 6 + opp % 3 + 1


def run(data):
    return sum(score1(m) for m in data.split('\n')), sum(score2(m) for m in data.split('\n'))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''A Y
B X
C Z'''

    test_a, test_b = run(sample)
    assert test_a == 15
    assert test_b == 12

    puz = Puzzle(2022, 2)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
