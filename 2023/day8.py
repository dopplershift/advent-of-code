from functools import reduce
from itertools import cycle
from aoc_tools import lcm


def parse(data):
    dirs, nodes = data.split('\n\n')
    tree = {}
    for line in nodes.split('\n'):
        src, dest = line.split(' = ')
        left, right = dest.split(', ')
        tree[src] = (left[1:], right[:-1])
    return dirs, tree


def part1(dirs, tree):
    dirs = cycle(dirs)

    count = 0
    loc = 'AAA'
    while loc != 'ZZZ':
        count += 1
        loc = tree[loc][next(dirs) == 'R']

    return count


def part2(dirs, tree):
    dirs = cycle(dirs)

    count = 0
    cycles = {}
    locs = [node for node in tree if node.endswith('A')]
    while not all(node.endswith('Z') for node in locs):
        count += 1
        choice = int(next(dirs) == 'R')
        new_locs = []
        for node in locs:
            node = tree[node][choice]
            new_locs.append(node)
            if node.endswith('Z'):
                if node not in cycles:
                    cycles[node] = count
                    new_locs.pop()
        locs = new_locs

    return reduce(lcm, cycles.values(), 1)


def run(data):
    dirs, tree = parse(data)

    return part1(dirs, tree), part2(dirs, tree)

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)'''

    test_a, test_b = run(sample)
    assert test_a == 2
    assert test_b == 2

    sample2 = '''LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''

    test_a, test_b = run(sample2)
    assert test_a == 6
    assert test_b == 6

    sample3 = '''LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)'''

    assert part2(*parse(sample3)) == 6

    puz = Puzzle(2023, 8)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
