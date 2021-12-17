import re


def parse(s):
    return tuple(map(int, re.search(r'x=([-\d]+)\.\.([-\d]+), y=([-\d]+)\.\.([-\d]+)', s, re.ASCII).groups()))


def get_track(u, v, right, bottom):
    x_trace = [0]
    y_trace = [0]
    x = 0
    y = 0
    for _ in range(10 * max(right, abs(bottom))):
        x += u
        y += v
        u += -1 if u > 0 else 1 if u < 0 else 0
        v -= 1
        x_trace.append(x)
        y_trace.append(y)
        if x > right or y < bottom:
            break
    else:
        print('Finished time without passing target')
    return x_trace, y_trace


def search_space(x_max, y_min):
    for v in range(y_min, -y_min):
        for u in range(0, x_max + 1):
            yield u, v


def find_trajectory(target):
    x_min, x_max, y_min, y_max = target
    highest = -2**30
    hits = set()
    for u, v in search_space(x_max, y_min):
        x, y = get_track(u, v, x_max, y_min)
        if any(x_min <= xi <= x_max and y_min <= yi <= y_max for xi, yi in zip(x, y)):
            highest = max(highest, max(y))
            hits.add((u, v))
    return highest, len(hits)


def run(data):
    region = parse(data)
    return find_trajectory(region)

if __name__ == '__main__':
    from aocd.models import Puzzle

    test_a, test_b = run('target area: x=20..30, y=-10..-5')
    assert test_a == 45
    assert test_b == 112

    puz = Puzzle(2021, 17)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
