import re


def parse(s):
    return tuple(map(int, re.findall(r'-?\d+', s, re.ASCII)))


def search_space(x_min, x_max, y_min):
    # Find the smallest x_velocity that still hits the left edge. This "integral" of velocity
    # is the sum n + (n - 1) + (n - 2) + ... + 1 -> n * (n + 1) / 2--I'm purposely trying to
    # avoid floating point math--hence no sqrt.
    u_min = 1
    while u_min * (u_min + 1) < 2 * x_min:
        u_min += 1

    for v in range(y_min, -y_min + 1):
        for u in range(u_min, x_max + 1):
            yield u, v


def find_trajectory(target):
    x_min, x_max, y_min, y_max = target

    highest_v = 0
    hits = 0
    for u, v in search_space(x_min, x_max, y_min):
        x = 0
        y = 0
        v_init = v
        # Stop when we get below or right of the target
        while x <= x_max and y >= y_min:
            # With loop condition, we only need to check if we're past left side and
            # below top edge.
            if x >= x_min and y <= y_max:
                highest_v = max(highest_v, v_init)
                hits += 1
                break
            x += u
            y += v
            u -= 1 if u > 0 else 0
            v -= 1

    # The biggest height is related to the "integral" of the ax upward velocity
    return (highest_v * (highest_v + 1)) // 2, hits


def run(data):
    region = parse(data)
    return find_trajectory(region)


if __name__ == '__main__':
    from aocd.models import Puzzle

    test_a, test_b = run('target area: x=20..30, y=-10..-5')
    assert test_a == 45
    assert test_b == 112

    puz = Puzzle(2021, 17)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
