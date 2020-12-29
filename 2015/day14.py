from collections import Counter
import re


def parse(s):
    table = {}
    for line in s.splitlines():
        name, speed, time, rest = re.match(r'(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds.', line).groups()
        table[name] = tuple(map(int, (speed, time, rest)))
    return table


def solve(table, n=1000):
    max_dist = 0
    for _, (speed, time, rest) in table.items():
        c, r = divmod(n, time + rest)
        dist = speed * (c * time + min(r, time))
        max_dist = max(dist, max_dist)
    return max_dist


def solve2(table, n=1000):
    scores = Counter()
    for i in range(1, n+1):
        max_dist = 0
        max_name = ''
        for name, (speed, time, rest) in table.items():
            c, r = divmod(i, time + rest)
            dist = speed * (c * time + min(r, time))
            if dist > max_dist:
                max_dist = dist
                max_name = name
            max_dist = max(dist, max_dist)
        scores[max_name] += 1
    return max(scores.values())


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''Comet can fly 14 km/s for 10 seconds, but then must rest for 127 seconds.
Dancer can fly 16 km/s for 11 seconds, but then must rest for 162 seconds.'''

    table = parse(t)
    assert solve(table) == 1120

    puz = Puzzle(2015, 14)

    puz.answer_a = solve(parse(puz.input_data), 2503)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve2(parse(puz.input_data), 2503)
    print(f'Part 2: {puz.answer_b}')