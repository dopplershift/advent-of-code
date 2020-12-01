import itertools
import math

def find_set(vals, num, target=2020):
    return next(filter(lambda i: sum(i) == target, itertools.combinations(vals, num)))

def solve(vals, num):
    return math.prod(find_set(vals, num))

if __name__ == '__main__':
    from aocd.models import Puzzle

    test_vals = [1721, 979, 366, 299, 675, 1456]
    assert set(find_set(test_vals, 2)) == {1721, 299}
    assert solve(test_vals, 2) == 514579

    assert set(find_set(test_vals, 3)) == {979, 366, 675}
    assert solve(test_vals, 3) == 241861950

    puz = Puzzle(2020, 1)
    nums = list(map(int, puz.input_data.split('\n')))

    puz.answer_a = solve(nums, 2)
    print('Part 1:', puz.answer_a)

    puz.answer_b = solve(nums, 3)
    print('Part 2:', puz.answer_b)