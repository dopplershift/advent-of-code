def extrap(seq):
    stack = [seq]
    while len(set(stack[-1])) > 1:
        diff = [b - a for a, b in zip(stack[-1][:-1], stack[-1][1:])]
        stack.append(diff)


    left = right = stack.pop()[-1]
    while stack:
        top = stack.pop()
        right = top[-1] + right
        left = top[0] - left

    return left, right


def parse(data):
    for line in data.split('\n'):
        yield list(map(int, line.split()))


def run(data):
    left_points, right_points = zip(*(extrap(seq) for seq in parse(data)))
    return sum(right_points), sum(left_points)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''0 3 6 9 12 15
    1 3 6 10 15 21
    10 13 16 21 30 45'''

    test_a, test_b = run(sample)
    assert test_a == 114
    assert test_b == 2

    puz = Puzzle(2023, 9)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
