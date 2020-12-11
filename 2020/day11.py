def parse(s):
    lookup = {'.': 0, 'L': 1, '#': 2}
    return [list(map(lookup.get, line)) for line in s.split('\n')]


def neighbors1(board, r, c):
    for y, x in [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]:
        if 0 <= y <= len(board) - 1 and 0 <= x <= len(board[y]) - 1:
            yield y, x

            
def solve(board, neighbors=neighbors1, occupied_limit=4):
    changed = True
    while changed:
        newboard = [[0] * len(row) for row in board]
        changed = False
        for r, row in enumerate(board):
            for c, spot in enumerate(row):
                if spot != 0:
                    sitting = sum(board[y][x] == 2 for y, x in neighbors(board, r, c))
                    if spot == 1 and sitting == 0:
                        spot = 2
                        changed = True
                    elif spot == 2 and sitting >= occupied_limit:
                        spot = 1
                        changed = True
                    newboard[r][c] = spot
        board = newboard
    return board


def neighbors2(board, r, c):
    for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        y = r + dy
        x = c + dx
        while 0 <= y <= len(board) - 1 and 0 <= x <= len(board[y]) - 1:
            if board[y][x] != 0:
                yield y, x
                break
            y += dy
            x += dx


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''L.LL.LL.LL
    LLLLLLL.LL
    L.L.L..L..
    LLLL.LL.LL
    L.LL.LL.LL
    L.LLLLL.LL
    ..L.L.....
    LLLLLLLLLL
    L.LLLLLL.L
    L.LLLLL.LL'''

    final = solve(parse(t))
    assert sum(i == 2 for row in final for i in row) == 37

    final2 = solve(parse(t), neighbors2, 5)
    assert sum(i == 2 for row in final2 for i in row) == 26

    n = neighbors2(parse('''.......#.
    ...#.....
    .#.......
    .........
    ..#L....#
    ....#....
    .........
    #........
    ...#.....'''), 4, 3)
    assert list(n) == [(2, 1), (1, 3), (0, 7), (4, 2), (4, 8), (7, 0), (8, 3), (5, 4)]

    puz = Puzzle(2020, 11)
    board = parse(puz.input_data)

    final = solve(board)
    puz.answer_a = sum(i == 2 for row in final for i in row)
    print(f'Part 1: {puz.answer_a}')

    final2 = solve(board, neighbors2, 5)
    puz.answer_b = sum(i == 2 for row in final2 for i in row)
    print(f'Part 1: {puz.answer_a}')