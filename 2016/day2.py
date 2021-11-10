def decode(lines, pad):
    moves = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}
    code = ''

    for loc, key in pad.items():
        if key == '5':
            break

    for line in lines:
        for move in line:
            dx, dy = moves[move]
            if (newloc := (loc[0] + dx, loc[1] + dy)) in pad:
                loc = newloc
        code += pad[loc]

    return code


if __name__ == '__main__':
    from aocd.models import Puzzle

    pad_part1 = {(0, 0): '1', (1, 0): '2', (2, 0): '3',
                 (0, 1): '4', (1, 1): '5', (2, 1): '6',
                 (0, 2): '7', (1, 2): '8', (2, 2): '9'}

    pad_part2 = {(2, 0): '1',
                 (1, 1): '2', (2, 1): '3', (3, 1): '4',
                 (0, 2): '5', (1, 2): '6', (2, 2): '7', (3, 2): '8', (4, 2): '9',
                 (1, 3): 'A', (2, 3): 'B', (3, 3): 'C',
                 (2, 4): 'D'}

    lines = 'ULL\nRRDDD\nLURDL\nUUUUD'.split('\n')
    assert decode(lines, pad_part1) == '1985'
    assert decode(lines, pad_part2) == '5DB3'

    puz = Puzzle(2016, 2)
    lines = puz.input_data.split('\n')

    puz.answer_a = decode(lines, pad_part1)
    print('Part 1:', puz.answer_a)

    puz.answer_b = decode(lines, pad_part2)
    print('Part 2:', puz.answer_b)
