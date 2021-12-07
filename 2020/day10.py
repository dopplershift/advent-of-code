from functools import lru_cache


def diffs(nums):
    return [x - y for y, x in zip(nums[:-1], nums[1:])]


def num_diffs(nums, diff):
    return sum(1 if d == diff else 0 for d in diffs(nums))


@lru_cache
# The number of paths from nums[cur] = sum(nums[cur + i] for i in (1, 2, 3) if valid_jump(i))
# Recursive solution that only runs quickly due to memoization
def count_paths(nums, cur=0):
    if cur == len(nums) - 1:
        return 1
    total = 0
    for n in range(cur + 1, len(nums)):
        if nums[n] - nums[cur] <= 3:
            total += count_paths(nums, n)
        else:
            break

    return total


# Instead of repeatedly walking forward and using caching, solve for increasingly larger
# values relying on the solution for smaller problems
# So here, the number of paths into nums[i] = sum(nums[i - j] for i in (1, 2, 3) if valid_jump(j))
def count_paths_dp(nums):
    dp = {nums[0]: 1}
    for n in nums[1:]:
        dp[n] = dp.get(n - 1, 0) + dp.get(n - 2, 0) + dp.get(n - 3, 0)
    return dp[nums[-1]]


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''28
    33
    18
    42
    31
    14
    46
    20
    48
    47
    24
    23
    49
    45
    19
    38
    39
    11
    1
    32
    25
    35
    8
    17
    7
    9
    4
    2
    34
    10
    3'''

    nums = [0] + sorted(map(int, t.split('\n')))
    nums += [max(nums) + 3]

    assert num_diffs(nums, 1) == 22
    assert num_diffs(nums, 3) == 10

    assert count_paths(tuple(nums)) == 19208
    assert count_paths_dp(tuple(nums)) == 19208

    puz = Puzzle(2020, 10)

    nums = [0] + sorted(map(int, puz.input_data.split('\n')))
    nums += [max(nums) + 3]

    puz.answer_a = num_diffs(nums, 1) * num_diffs(nums, 3)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = count_paths(tuple(nums))
    print(f'Part 2: {puz.answer_b}')
