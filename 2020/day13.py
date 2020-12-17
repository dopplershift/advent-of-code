def parse(s):
    time, ids = s.split('\n')
    return int(time), list(map(lambda i: int(i) if i != 'x' else -1, ids.split(',')))


def solve(time, ids):
    min_id = 0
    next_arrive = 0
    wait = 2**32
    for i in ids:
        if i == -1:
            continue
        rem = i - time % i
        if rem < wait:
            min_id = i
            wait = rem
    return min_id * wait


# Wikipedia: Chinese Remainder Theorem
def find_time(ids):
    options = sorted([(i, offset) for offset, i in enumerate(ids) if i != -1])
    inc, off = options.pop()
    next_time = inc - off
    # Essentially solve a bus, then step through to solve the next, using the product
    # of solved busses as the step--relying on the fact that all the numbers were
    # relatively prime. Otherwise, would need to use lcm() of them.
    for repeat, wait in reversed(options):
        while (next_time + wait) % repeat:
            next_time += inc
        inc *= repeat
    return next_time


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''939
    7,13,x,x,59,x,31,19'''

    time, ids = parse(t)

    assert solve(time, ids) == 295
    assert find_time(ids) == 1068781

    assert find_time([17,-1,13,19]) == 3417
    assert find_time([67,7,59,61]) == 754018
    assert find_time([67,-1,7,59,61]) == 779210
    assert find_time([67,7,-1,59,61]) == 1261476
    assert find_time([1789,37,47,1889]) == 1202161486

    puz = Puzzle(2020, 13)
    time, ids = parse(puz.input_data)

    puz.answer_a = solve(time, ids)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_time(ids)
    print(f'Part 2: {puz.answer_b}')