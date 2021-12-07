def parse(s):
    for line in s.split('\n'):
        yield line.strip()[0], int(line.strip()[1:])


def do_ship(comms):
    x, y = (0, 0)
    dx, dy = 1, 0
    for c, l in comms:
        if c == 'N':
            y += l
        elif c == 'S':
            y -= l
        elif c == 'E':
            x += l
        elif c == 'W':
            x -= l
        elif c == 'F':
            x += dx * l
            y += dy * l
        elif c == 'L':
            while l > 0:
                dx, dy = -dy, dx
                l -= 90
        elif c == 'R':
            while l > 0:
                dx, dy = dy, -dx
                l -= 90
    return abs(x) + abs(y)


def follow_waypoint(comms):
    way_x, way_y = 10, 1
    ship_x, ship_y = 0, 0
    for c, l in comms:
        if c == 'N':
            way_y += l
        elif c == 'S':
            way_y -= l
        elif c == 'E':
            way_x += l
        elif c == 'W':
            way_x -= l
        elif c == 'F':
            ship_x += way_x * l
            ship_y += way_y * l
        elif c == 'L':
            while l > 0:
                way_x, way_y = -way_y, way_x
                l -= 90
        elif c == 'R':
            while l > 0:
                way_x, way_y = way_y, -way_x
                l -= 90
    return abs(ship_x) + abs(ship_y)


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''F10
    N3
    F7
    R90
    F11'''

    commands = list(parse(t))

    assert do_ship(commands) == 25
    assert follow_waypoint(commands) == 286

    puz = Puzzle(2020, 12)
    commands = list(parse(puz.input_data))

    puz.answer_a = do_ship(commands)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = follow_waypoint(commands)
    print(f'Part 1: {puz.answer_b}')
