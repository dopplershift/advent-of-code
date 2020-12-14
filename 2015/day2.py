import itertools
import math

def parse(s):
    for line in s.split('\n'):
        yield list(map(int, line.split('x')))


def part1(s):
    total = 0
    for dims in parse(s):
        areas = list(map(lambda x: x[0] * x[1], itertools.permutations(dims, 2)))
        total += sum(areas) + min(areas)
    return total


def part2(s):
    total = 0
    for dims in parse(s):
        perims = list(map(lambda x: 2 * (x[0] + x[1]), itertools.permutations(dims, 2)))
        total += min(perims) + math.prod(dims)
    return total


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2015, 2)
    
    puz.answer_a = part1(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(puz.input_data)
    print(f'Part 2: {puz.answer_b}')