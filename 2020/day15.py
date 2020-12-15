def parse(s):
    return list(map(int, s.split(',')))


def solve(nums, end=2020):
    last_spoken = {n:i for i, n in enumerate(nums)}

    # Fine so long as we don't repeat in the initial digits
    next_val = 0
    for t in range(len(nums), end):
        cur = next_val
        next_val = t - last_spoken[cur] if cur in last_spoken else 0
        last_spoken[cur] = t
    return cur


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''0,3,6'''
    assert solve(parse(t)) == 436

    assert solve([1, 3, 2]) == 1
    assert solve([2, 1, 3]) == 10
    assert solve([1, 2, 3]) == 27
    assert solve([2, 3, 1]) == 78
    assert solve([3, 2, 1]) == 438
    assert solve([3, 1, 2]) == 1836

    puz = Puzzle(2020, 15)
    nums = parse(puz.input_data)

    puz.answer_a = solve(nums)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve(nums, 30000000)
    print(f'Part 2: {puz.answer_b}')