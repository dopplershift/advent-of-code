def parse(s):
    return list(map(int, s.split(',')))


def solve(nums, end=2020):
    d = dict()
    for i, n in enumerate(nums):
        d.setdefault(n, []).append(i)
    turns = nums.copy()

    for i in range(len(nums), end):
        last = turns[-1]
        prev = d[last]
        if len(prev) < 2:
            turns.append(0)
        else:
            turns.append(prev[-1] - prev[-2])
        d.setdefault(turns[-1], []).append(i)
    return turns[-1]


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''0,3,6'''
    assert solve(parse(t)) == 436
    assert solve([2, 1, 3]) == 10
    assert solve([3, 1, 2]) == 1836

    puz = Puzzle(2020, 15)
    nums = parse(puz.input_data)

    puz.answer_a = solve(nums)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve(nums, 30000000)
    print(f'Part 2: {puz.answer_b}')