from itertools import cycle
from geom import Point, Vector

def moves(steps):
    for step in steps:
        yield step[0], int(step[1:])

def walk(steps):
    loc = Point(0, 0)
    direc = Vector(0, 1, 0)
    for turn, dist in moves(steps):
        if turn == 'R':
            direc = -Vector.k().cross(direc)
        else:
            direc = direc.cross(-Vector.k())
        loc += dist * direc

    return loc


def walk2(steps):
    loc = Point(0, 0)
    visited = {loc}
    direc = Vector(0, 1, 0)
    for turn, dist in cycle(moves(steps)):
        if turn == 'R':
            direc = -Vector.k().cross(direc)
        else:
            direc = direc.cross(-Vector.k())
        for _ in range(dist):
            loc += direc
            if loc in visited:
                return loc
            else:
                visited.add(loc)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert walk(['R2', 'L3']).manhattan_distance(Point(0, 0)) == 5
    assert walk(['R2', 'R2', 'R2']).manhattan_distance(Point(0, 0)) == 2
    assert walk(['R5', 'L5', 'R5', 'R3']).manhattan_distance(Point(0, 0)) == 12
    assert walk2(['R8', 'R4', 'R4', 'R8']).manhattan_distance(Point(0, 0)) == 4

    puz = Puzzle(2016, 1)
    steps = puz.input_data.split(', ')

    puz.answer_a = walk(steps).manhattan_distance(Point(0, 0))
    print('Part 1:', puz.answer_a)

    puz.answer_b = walk2(steps).manhattan_distance(Point(0, 0))
    print('Part 2:', puz.answer_b)