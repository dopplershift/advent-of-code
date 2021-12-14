def run(data):
    locs = parse(data)
    return solve(locs), solve(locs, cost2)


def parse(s):
    return list(map(int, s.split(',')))


def cost1(target, current):
    return abs(target - current)


def cost2(target, current):
    diff = abs(target - current)
    return (diff * (diff + 1)) // 2


def solve(nums, cost_func=cost1):
    return min(sum(cost_func(i, n) for n in nums)
               for i in range(min(nums), max(nums) + 1))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '16,1,2,0,4,2,7,1,2,14'

    test_a, test_b = run(sample)
    assert test_a == 37
    assert test_b == 168

    puz = Puzzle(2021, 7)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
