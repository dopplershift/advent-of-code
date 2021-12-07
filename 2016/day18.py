from itertools import chain


def parse(s):
    return tuple(c == '^' for c in s)


def next_row(row):
    return tuple(a != b for a,b in zip(chain([False], row),
                                       chain(row[1:], [False])))


def count(row, n):
    total = 0
    for _ in range(n):
        total += sum(row)
        row = next_row(row)
    return len(row) * n - total


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert next_row((False, False, True, True, False)) == (False, True, True, True, True)
    assert next_row((False, True, True, True, True)) == (True, True, False, False, True)
    assert count(parse('.^^.^.^^^^'), 10) == 38

    puz = Puzzle(2016, 18)
    row = parse(puz.input_data)

    puz.answer_a = count(row, 40)
    print('Part 1:', puz.answer_a)

    puz.answer_b = count(row, 400000)
    print('Part 2:', puz.answer_b)
