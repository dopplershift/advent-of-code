def cycle_board(board):
    seq = set()
    while True:
        if tuple(board) in seq:
            break
        seq.add(tuple(board))
        next_board = []
        for r, line in enumerate(board):
            row = []
            for c, char in enumerate(line):
                count = 0
                if r > 0 and board[r - 1][c] == '#':
                    count += 1
                if r < len(board) - 1 and board[r + 1][c] == '#':
                    count += 1
                if c > 0 and board[r][c - 1] == '#':
                    count += 1
                if c < len(board[0]) - 1 and board[r][c + 1] == '#':
                    count += 1

                if char == '#' and count != 1:
                    char = '.'
                elif char == '.' and count in (1, 2):
                    char = '#'
                row.append(char)

            next_board.append(''.join(row))
        board = next_board
    return board


def run_board_recursive(board, size, minutes):
    middle = size // 2
    half_above = middle - 1
    half_below = middle + 1
    min_depth = max_depth = 0

    for minute in range(minutes):
        depths = [k[0] for k in board]
        min_depth = min(depths) - 1
        max_depth = max(depths) + 1
        next_board = set()
        for depth in range(min_depth, max_depth + 1):
            for r in range(size):
                for c in range(size):
                    # Middle is no longer a space
                    if r == middle and c == middle:
                        continue

                    neighbors = []

                    # Above
                    if r == 0:
                        neighbors.append((depth - 1, half_above, middle))
                    elif r == half_below and c == middle:
                        neighbors.extend((depth + 1, size - 1, i) for i in range(size))
                    else:
                        neighbors.append((depth, r - 1, c))

                    # Below
                    if r == size - 1:
                        neighbors.append((depth - 1, half_below, middle))
                    elif r == half_above and c == middle:
                        neighbors.extend((depth + 1, 0, i) for i in range(size))
                    else:
                        neighbors.append((depth, r + 1, c))

                    # Left
                    if c == 0:
                        neighbors.append((depth - 1, middle, half_above))
                    elif c == half_below and r == middle:
                        neighbors.extend((depth + 1, i, size - 1) for i in range(size))
                    else:
                        neighbors.append((depth, r, c - 1))

                    # Right
                    if c == size - 1:
                        neighbors.append((depth - 1, middle, half_below))
                    elif c == half_above and r == middle:
                        neighbors.extend((depth + 1, i, 0) for i in range(size))
                    else:
                        neighbors.append((depth, r, c + 1))

                    is_bug = (depth, r, c) in board
                    bugs = sum(n in board for n in neighbors)

                    if (is_bug and bugs == 1) or (not is_bug and bugs in (1, 2)):
                        next_board.add((depth, r, c))

        board = next_board
    return board


if __name__ == '__main__':
    from aocd.models import Puzzle
    
    puz = Puzzle(2019, 24)
    board = cycle_board(puz.input_data.split('\n'))
    puz.answer_a = sum(2**i for i, c in enumerate(''.join(board)) if c == '#')
    print(f'Part 1: {puz.answer_a}')

    board = {(0, r, c)
             for r, line in enumerate(puz.input_data.split('\n'))
             for c, char in enumerate(line.strip())
             if char == '#'}
    size = len(puz.input_data.split('\n')[0])

    board = run_board_recursive(board, size, 200)
    puz.answer_b = len(board)
    print(f'Part 2: {puz.answer_b}')