from aoc_tools import ocr
from geom import Point, Vector
from intcode import Computer


def run(data):
    codes = [int(c) for c in data.split(',')]
    return len(paint(codes)), ocr(to_image(paint(codes, start=1)))


def paint(codes, start=0):
    c = Computer(codes)

    loc = Point(0, 0)
    direc = Vector(0, 1, 0)
    panels = {loc:start}
    while c.running:
        c.run([panels.get(loc, 0)])
        turn = c.output.pop()
        color = c.output.pop()
        panels[loc] = color

        if turn == 0: # Turn left
            direc = Vector.k().cross(direc)
        elif turn == 1: # Turn right
            direc = direc.cross(Vector.k())

        loc += direc
    return panels


def to_image(panels):
    min_row = min(panels.keys(), key=lambda i:i.y).y
    max_row = max(panels.keys(), key=lambda i:i.y).y
    min_col = min(panels.keys(), key=lambda i:i.x).x
    max_col = max(panels.keys(), key=lambda i:i.x).x

    return '\n'.join(''.join('#' if panels.get(Point(col, row), 0) == 1 else ' ' for col in range(min_col, max_col + 1))
                             for row in range(max_row, min_row - 1, -1))


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 11)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
