pipe_dirs = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE'}
opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}
deltas = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}

def walk(grid):
    for loc, val in grid.items():
        if val == 'S':
            path = [loc]
            break

    for cur_dir in 'NESW':
        dx, dy = deltas[cur_dir]
        check = (path[-1][0] + dx, path[-1][1] + dy)
        if (p := grid.get(check, '.')) != '.' and opposite[cur_dir] in pipe_dirs[p]:
            path.append(check)
            break

    while (tile := grid[path[-1]]) != 'S':
        # Follow the pipe to change direction
        cur_dir = pipe_dirs[tile].replace(opposite[cur_dir], '')

        # Move
        dx, dy = deltas[cur_dir]
        path.append((path[-1][0] + dx, path[-1][1] + dy))


    return path


def parse(data):
    return {(x, y): c for y, row in enumerate(data.split('\n')) for x, c in enumerate(row)}


def interior(path):
    inside_area = perim = 0
    prev_x, prev_y = path[-1]
    for x, y in path:
        dx = x - prev_x
        dy = y - prev_y
        prev_x, prev_y = x, y

        # Trapezoid/shoelace area formula reduce to our right angle polygon
        inside_area += y * dx
        perim += abs(dx) + abs(dy)

    # Combine with Pick's Theorem for area of a polygon with integer vertices
    # A = intererior + boundary / 2 - 1 -> interior = A - b / 2 + 1
    return abs(inside_area) - perim // 2 + 1


def run(data):
    grid = parse(data)
    path = walk(grid)
    path_set = set(path)

    return len(path) // 2, interior(path)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''-L|F7
7S-7|
L|7||
-L-J|
L|-JF'''

    test_a, test_b = run(sample)
    assert test_a == 4
    assert test_b == 1

    sample2 = '''7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ'''
    test_a, test_b = run(sample2)
    assert test_a == 8
    assert test_b == 1

    sample3 = '''...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........'''
    _, test_b = run(sample3)
    assert test_b == 4

    sample4 = '''.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...'''
    _, test_b = run(sample4)
    assert test_b == 8

    sample5 = '''FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L'''
    _, test_b = run(sample5)
    assert test_b == 10

    puz = Puzzle(2023, 10)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
