from geom import Point, Vector
from intcode import Computer, readcode


class CheckPoint:
    def __init__(self, source):
        self.prog = [int(c) for c in source.split(',')]
        self.comp = Computer(self.prog)

    def __call__(self, inp):
        self.comp.reset(self.prog)
        self.comp.run(inp)
        return self.comp.output[0]


def scan(cp):
    total = 0
    for x in range(50):
        for y in range(50):
            total += cp((x, y))

    return total


def find_location(cp):
    right = Vector(1, 0, 0)
    down = Vector(0, 1, 0)

    loc = Point(0, 0)
    size = 100
    right_edge = Vector(size - 1, 0, 0)
    bottom_edge = Vector(0, size - 1, 0)

    while not (cp(loc + right_edge) and cp (loc + bottom_edge)):
        while not cp(loc + bottom_edge):
            loc += right
        while not cp(loc + right_edge):
            loc += down

    return loc


def run(data):
    cp = CheckPoint(data)
    part_a = scan(cp)

    loc = find_location(cp)
    part_b = 10000 * loc.x + loc.y

    return part_a, part_b


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 19)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
