def area(plan):
    dir_map = {'R': (1, 0), 'L': (-1, 0), 'U': (0, 1), 'D': (0, -1)}
    inside_area = perim = 0
    x, y = 0, 0
    for direc, l in plan:
        dx, dy = dir_map[direc]
        x += dx * l
        y += dy * l

        # Trapezoid/shoelace area formula reduce to our right angle polygon
        inside_area += y * l * dx
        perim += l

    # Combine with Pick's Theorem for area of a polygon with integer vertices
    # A = intererior + boundary / 2 - 1 -> interior = A - b / 2 + 1
    # total = A + boundary -> A + b / 2 + 1 -> A + perim / 2 + 1
    return inside_area + perim // 2 + 1


def parse(data, use_rgb=False):
    for line in data.split('\n'):
        d, l, rgb = line.split()
        if use_rgb:
            yield 'RDLU'[int(rgb[-2])], int(rgb[2:7], 16)
        else:
            yield d, int(l)


def run(data):
    return area(parse(data)), area(parse(data, use_rgb=True))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = r'''R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)'''

    test_a, test_b = run(sample)
    assert test_a == 62
    assert test_b == 952408144115

    puz = Puzzle(2023, 18)

    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
