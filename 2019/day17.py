from geom import Point, Vector
from intcode import Computer


def parse_output(out):
    layout = [[]]
    for i in out:
        char = chr(i)
        if char == '\n':
            layout.append([])
        else:
            layout[-1].append(char)
            if char in '<^>V':
                robot = (len(layout[-1]) - 1, len(layout) - 1, char)
    while not layout[-1]:
        layout.pop()
    return layout, robot


def print_board(board):
    print('\n'.join([''.join(c for c in row) for row in board]))


def valid_index(layout, point):
    return point.y >= 0 and point.y < len(layout) and point.x >=0 and point.x < len(layout[0]) 


def walk_scaffold(layout, robot):
    direcs = {'>':Vector(1, 0, 0), '<':Vector(-1, 0, 0), '^':Vector(0, -1, 0), 'V':Vector(0, 1, 0)}
    scaffold = '#'

    cur_loc = Point(*robot[:2])
    cur_dir = direcs[robot[-1]]
    cur_run = 0
    moves = []
    while True:
        #print(cur_loc, cur_dir)
        next_loc = cur_loc + cur_dir
        if valid_index(layout, next_loc) and layout[next_loc.y][next_loc.x] == scaffold:
            cur_loc = next_loc
            cur_run += 1
        else:
            if cur_run:
                moves.append(cur_run)
                cur_run = 0

            # All of the directions are kinda flipped from expected because we're in a coordinate system
            # where +y is down.
            if cur_dir.x == 1:
                left = cur_loc.down
                right = cur_loc.up
            elif cur_dir.x == -1:
                left = cur_loc.up
                right = cur_loc.down
            elif cur_dir.y == 1:
                left = cur_loc.right
                right = cur_loc.left
            elif cur_dir.y == -1:
                left = cur_loc.left
                right = cur_loc.right

            if valid_index(layout, left) and layout[left.y][left.x] == scaffold:
                moves.append('L')
                cur_dir = cur_dir.cross(Vector.k())
            elif valid_index(layout, right) and layout[right.y][right.x] == scaffold:
                moves.append('R')
                cur_dir = Vector.k().cross(cur_dir)
            else:
                break

    return ','.join(str(i) for i in moves)


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 17)
    c = Computer.fromstring(puz.input_data)
    c.run()
    layout, robot = parse_output(c.output)
    # print_board(layout)

    v = sum(r * c for r in range(1, len(layout) - 1)
                  for c in range(1, len(layout[0]) - 1)
                  if {layout[r][c], layout[r + 1][c], layout[r - 1][c], layout[r][c - 1], layout[r][c + 1]} == {'#'})
    puz.answer_a = v
    print(f'Part 1: {puz.answer_a}')

    move_str = walk_scaffold(layout, robot)

    # Emprically determined
    sub_a = 'R,10,R,8,L,10,L,10'
    sub_b = 'R,8,L,6,L,6'
    sub_c = 'L,10,R,10,L,6'
    main = move_str.replace(sub_a, 'A').replace(sub_b, 'B').replace(sub_c, 'C')

    c = Computer.fromstring(puz.input_data)
    c.memory[0] = 2
    c.run(main + '\n' + sub_a + '\n' + sub_b + '\n' + sub_c + '\nn\n')
    # c.display_ascii()
    puz.answer_b = c.output[-1]
    print(f'Part 2: {puz.answer_b}')