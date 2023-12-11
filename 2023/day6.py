import math

def options(t, d):
    # h = hold
    # h * (t - h) = d -> -h^2 + t * h - d = 0
    disc = math.sqrt(t * t - 4 * d)
    l = (t - disc) / 2
    r = (t + disc) / 2
    # Slight adjustment to handle if roots are actually integers, we want to exclude those
    # sine they don't *beat* the record
    return int(math.floor(r - 0.001) - math.ceil(l + 0.001) + 1)


def parse(data):
    lines = data.split('\n')
    times = list(map(int, lines[0].split()[1:]))
    distances = list(map(int, lines[1].split()[1:]))
    return times, distances


def run(data):
    times, dists = parse(data)

    margin = 1
    for t, d in zip(times, dists):
        margin *= options(t, d)

    big_time = int(''.join(str(i) for i in times))
    big_dist = int(''.join(str(d) for d in dists))
    return margin, options(big_time, big_dist)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''Time:      7  15   30
Distance:  9  40  200'''

    test_a, test_b = run(sample)
    assert test_a == 288
    assert test_b == 71503

    puz = Puzzle(2023, 6)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
