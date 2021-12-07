import math


def trees(board, slope):
    max_y = len(board)
    max_x = len(board[0])
    locx, locy = (0, 0)
    slope_x, slope_y = slope
    count = 0
    while locy < max_y:
        if board[locy][locx] == '#':
            count += 1
        locx = (locx + slope_x) % max_x
        locy += slope_y
    return count


def solve2(board):
    return math.prod(trees(board, slope) for slope in [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)])


if __name__ == '__main__':
    from aocd.models import Puzzle

    s = '''..##.......
    #...#...#..
    .#....#..#.
    ..#.#...#.#
    .#...##..#.
    ..#.##.....
    .#.#.#....#
    .#........#
    #.##...#...
    #...##....#
    .#..#...#.#'''

    # Need strip() due to indentation
    board = [line.strip() for line in s.split('\n')]

    assert trees(board, (1, 1)) == 2
    assert trees(board, (3, 1)) == 7
    assert trees(board, (5, 1)) == 3
    assert trees(board, (7, 1)) == 4
    assert trees(board, (1, 2)) == 2

    assert solve2(board) == 336

    puz = Puzzle(2020, 3)
    field = puz.input_data.split('\n')

    puz.answer_a = trees(field, (3, 1))
    print('Part 1:', puz.answer_a)

    puz.answer_b = solve2(field)
    print('Part 2:', puz.answer_b)
