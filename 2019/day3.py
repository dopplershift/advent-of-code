def solve(line1, line2):
    wire1 = make_paths(line1.split(','))
    wire2 = make_paths(line2.split(','))
    return min(abs(pt[0]) + abs(pt[1]) for pt in find_intersections(wire1, wire2))


def find_intersections(wire1, wire2):
    for seg1 in wire1:
        for seg2 in wire2:
            pt = intersects(seg1, seg2)
            if pt is not None and pt != (0, 0):
                yield pt

                
def intersects(seg1, seg2):
    direc1, fixed1, b0_1, b1_1, dist1 = seg1
    direc2, fixed2, b0_2, b1_2, dist2 = seg2
    if fixed1 == 0 and fixed2 == 0:
        return

    if (direc1 in ('L', 'R') and direc2 in ('L', 'R')) or (direc1 in ('U', 'D') and direc2 in ('U', 'D')):
        if fixed1 == fixed2:
            print('here!')
    elif fixed1 >= b0_2 and fixed1 <= b1_2 and fixed2 >= b0_1 and fixed2 <= b1_1:
        off1 = fixed1 - b0_2 if direc2 in ('U', 'R') else b1_2 - fixed1
        off2 = fixed2 - b0_1 if direc1 in ('U', 'R') else b1_1 - fixed2
        if direc1 in ('L', 'R'):
            return fixed2, fixed1, dist1 + dist2 + off1 + off2
        elif direc2 in ('L', 'R'):
            return fixed1, fixed2, dist1 + dist2 + off1 + off2


def make_paths(moves):
    cur_x = 0
    cur_y = 0
    paths = []
    total = 0
    for step in moves:
        direc = step[0]
        dist = int(step[1:])
        next_x = cur_x
        next_y = cur_y
        if direc == 'L':
            next_x -= dist
            paths.append((direc, cur_y, min(cur_x, next_x), max(cur_x, next_x), total))
        elif direc == 'R':
            next_x += dist
            paths.append((direc, cur_y, min(cur_x, next_x), max(cur_x, next_x), total))
        elif direc == 'U':
            next_y += dist
            paths.append((direc, cur_x, min(cur_y, next_y), max(cur_y, next_y), total))
        elif direc == 'D':
            next_y -= dist
            paths.append((direc, cur_x, min(cur_y, next_y), max(cur_y, next_y), total))
        total += dist
        cur_x, cur_y = next_x, next_y
    return paths


def solve2(line1, line2):
    wire1 = make_paths(line1.split(','))
    wire2 = make_paths(line2.split(','))
    return min(pt[2] for pt in find_intersections(wire1, wire2))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert solve('R8,U5,L5,D3', 'U7,R6,D4,L4') == 6
    assert solve('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 159
    assert solve('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 135

    assert solve2('R8,U5,L5,D3', 'U7,R6,D4,L4') == 30
    assert solve2('R75,D30,R83,U83,L12,D49,R71,U7,L72', 'U62,R66,U55,R34,D71,R55,D58,R83') == 610
    assert solve2('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51', 'U98,R91,D20,R16,D67,R40,U7,R15,U6,R7') == 410

    puz = Puzzle(2019, 3)
    puz.answer_a = solve(*puz.input_data.split('\n'))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve2(*puz.input_data.split('\n'))
    print(f'Part 2: {puz.answer_b}')