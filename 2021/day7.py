def parse(s):
    return list(map(int, s.split(',')))


def cost1(target, current):
    return abs(target - current)


def cost2(target, current):
    diff = abs(target - current)
    return (diff * (diff + 1)) // 2


def solve(nums, cost_func=cost1):
    min_pos = -1
    min_total = 2**32
    for i in range(min(nums), max(nums) + 1):
        total = sum(cost_func(i, n) for n in nums)
        if total < min_total:
            min_total = total
            min_pos = i
    return min_pos, min_total


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '16,1,2,0,4,2,7,1,2,14'
    assert solve(parse(sample)) == (2, 37)
    assert solve(parse(sample), cost2) == (5, 168)

    puz = Puzzle(2021, 7)

    puz.answer_a = solve(parse(puz.input_data))[-1]
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve(parse(puz.input_data), cost2)[-1]
    print(f'Part 2: {puz.answer_b}')