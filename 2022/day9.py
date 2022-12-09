def parse(data):
    return [(l[0], int(l[2:])) for l in data.split('\n')]


def simulate(moves, length):
    rope = [(0, 0)] * length
    history = {rope[-1]}
    dirs = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
    for d, n in moves:
        dx, dy = dirs[d]
        for i in range(n):
            newrope = [(rope[0][0] + dx, rope[0][1] + dy)]
            for knot in rope[1:]:
                newrope.append(follow(newrope[-1], knot))
            rope = newrope
            history.add(rope[-1])
    return history


def follow(head, tail):
    dx = head[0] - tail[0]
    dy = head[1] - tail[1]
    mx = my = 0
    if abs(dx) > 1:
        mx = 1 if dx > 0 else -1
        if dy:
            my = 1 if dy > 0 else -1
    elif abs(dy) > 1:
        my = 1 if dy > 0 else -1
        if dx:
            mx = 1 if dx > 0 else -1

    return (tail[0] + mx, tail[1] + my)


def run(data):
    moves = parse(data)
    return len(simulate(moves, 2)), len(simulate(moves, 10))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''
    test_a, test_b = run(sample)
    assert test_a == 13
    assert test_b == 1

    sample2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''
    test_a, test_b = run(sample2)
    assert test_a == 88
    assert test_b == 36

    puz = Puzzle(2022, 9)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
