def solve(s, n):
    s = list(map(int, s))
    for _ in range(n):
        queue = iter(s)
        next_s = []
        while c := next(queue, None):
            if next_s and c == next_s[-1]:
                next_s[-2] += 1
            else:
                next_s.extend((1, c))
        s = next_s
    return ''.join(str(i) for i in s)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert solve('1', 5) == '312211'

    puz = Puzzle(2015, 10)

    puz.answer_a = len(solve(puz.input_data, 40))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = len(solve(puz.input_data, 50))
    print(f'Part 2: {puz.answer_b}')
