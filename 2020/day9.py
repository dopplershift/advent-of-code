import collections
import itertools


def find_bad(vals, size):
    for i, val in enumerate(vals[size:]):
        sums = set(map(sum, itertools.combinations(vals[i:i+size], 2)))
        if val not in sums:
            return val


# Brute force--was surprisingly fast enough
# Check windows of all sizes, moving them all over the list
# The way this is written is basically O(N^2)
def find_run(vals, target):
    for size in range(2, len(vals)):
        for start in range(0, len(vals) - size):
            if sum(vals[start:start + size]) == target:
                return vals[start:start + size]


# Much smarter way to do this
# This is roughly O(N)--42x faster on my input of 1000 numbers
def find_run_fast(vals, target):
    # Adjustable window for the current group of numbers
    window = collections.deque()

    # Use an iterator over our list of values
    val_iter = iter(vals)
    total = 0

    # "Infinite" loop will break with StopIteration from iterator if we
    # don't find the total
    while True:
        # While the total is too small, get a new value and add to the total and
        # to the window on the right
        while total < target:
            next_val = next(val_iter)
            total += next_val
            window.append(next_val)

        # While the total is too big, drop numbers from the left side of the window
        # and subtract them from the total
        while total > target:
            total -= window.popleft()

        # Check whether we hit the target and have enough values
        if total == target and len(window) >= 2:
            return window


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576'''
    nums = list(map(int, t.split('\n')))

    assert find_bad(nums, 5) == 127
    assert find_run(nums, 127) == [15, 25, 47, 40]
    assert list(find_run_fast(nums, 127)) == [15, 25, 47, 40]

    puz = Puzzle(2020, 9)
    nums = list(map(int, puz.input_data.split('\n')))

    target = find_bad(nums, 25)
    puz.answer_a = target
    print(f'Part 1: {puz.answer_a}')

    run = find_run(nums, target)
    puz.answer_b = min(run) + max(run)
    print(f'Part 2: {puz.answer_b}')
