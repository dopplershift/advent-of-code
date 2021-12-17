import itertools
import re


def parse(s):
    return tuple(map(int, re.findall(r'-?\d+', s, re.ASCII)))


def get_xtrack(u, right, n, start=0):
    x_trace = [start]
    while x_trace[-1] <= right and len(x_trace) < n:
        x_trace.append(x_trace[-1] + u)
        # Only need to handle u >= 0--nothing turns it < 0
        u -= 1 if u > 0 else 0
        if u == 0:
            x_trace.extend([x_trace[-1]] * (n - len(x_trace)))
            break
    return x_trace


def get_ytrack(v, bottom, start=0):
    y_trace = [start]
    while y_trace[-1] >= bottom:
        y_trace.append(y_trace[-1] + v)
        v -= 1
    return y_trace


def find_trajectory(target):
    x_min, x_max, y_min, y_max = target

    # Range for y: Going up at -y_min (+ve) means it comes back down at y=0 with v=y_min
    # Something moving at v=y_min is the fastest downwards that intersects the target--it
    # intersects right at bottom at y=y_min.
    y_paths = [(v, get_ytrack(v, y_min)) for v in range(y_min, -y_min + 1)]
    max_steps = max(len(p[1]) for p in y_paths)

    # Find the smallest x_velocity that still hits the left edge. This "integral" of velocity
    # is the sum n + (n - 1) + (n - 2) + ... + 1 -> n * (n + 1) / 2--I'm purposely trying to
    # avoid floating point math--hence no sqrt.
    u_min = 0
    while u_min * (u_min + 1) < 2 * x_min:
        u_min += 1

    # Max x velocity that still hits is moving at x_max--in 1 step it hits the right edge
    x_paths = [get_xtrack(u, x_max, max_steps) for u in range(u_min, x_max + 1)]

    # Now that we know all the possible individual path options for different starting velocities
    # in x or y, we can consider each pair and see if they have a point in the target.
    highest_v = 0
    hits = 0
    for x, (v, y) in itertools.product(x_paths, y_paths):
        if any(x_min <= xi <= x_max and y_min <= yi <= y_max for xi, yi in zip(x, y)):
            highest_v = max(highest_v, v)
            hits += 1

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
