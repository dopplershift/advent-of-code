from itertools import chain, tee
from array import array


def pairwise_circle(iterable):
    a, b = tee(iterable)
    return zip(a, chain(b, [next(b, None)]))


def do_moves(cups, n):
    # Using a dictionary as a linked list between one cup and its clockwise
    # neighbor--one that can be accessed O(1) by label
#     clockwise = {l:r for l, r in pairwise_circle(cups)}
    # Switching to an array of integers is 40% faster (6.4s -> 3.8s)
    clockwise = array('I', [0] * (len(cups) + 1))
    for l, r in pairwise_circle(cups):
        clockwise[l] = r
    current = cups[0]

    max_cup = max(cups)
    for _ in range(n):
        first_rm = clockwise[current]
        mid_rm = clockwise[first_rm]
        last_rm = clockwise[mid_rm]

        # Find destination
        # Using ternary is faster than adjusted modulus
        # desired = (current - 2) % max_cup + 1
        desired = current - 1 if current > 1 else max_cup
        while desired in (first_rm, mid_rm, last_rm):
            desired = desired - 1 if desired > 1 else max_cup

        # Point clockwise to the one that was clockwise of the last one removed
        # and also update our current pointer to that same one
        clockwise[current] = current = clockwise[last_rm]

        # Splice in the removed ones in the right spot
        clockwise[last_rm] = clockwise[desired]
        clockwise[desired] = first_rm

    return clockwise


def solve1(cups, n=100):
    cups = do_moves(cups, n)
    node = 1
    val = ''
    while (node := cups[node]) != 1:
        val += str(node)
    return val


def solve2(cups, n):
    cups = do_moves(cups, n)
    n1 = cups[1]
    n2 = cups[n1]
    return n1 * n2


if __name__ == '__main__':
    from aocd.models import Puzzle

    nums = list(map(int, '389125467'))
    assert solve1(nums, 10) == '92658374'
    assert solve1(nums, 100) == '67384529'

    nums = list(map(int, '389125467')) + list(range(10, 1000000 + 1))
    assert solve2(nums, 10_000_000) == 149245887792

    puz = Puzzle(2020, 23)

    puz.answer_a = solve1(list(map(int, puz.input_data)))
    print(f'Part 1: {puz.answer_a}')

    nums = list(map(int, puz.input_data)) + list(range(10, 1000000 + 1))
    puz.answer_b = solve2(nums, 10000000)
    print(f'Part 2: {puz.answer_b}')
