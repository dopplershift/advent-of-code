def parse(s):
    return tuple(c == '^' for c in s)


def get_trap(row, ind):
    start = max(ind - 1, 0)
    relevant = row[start: ind + 2]
    return ((sum(relevant) == 1 and not row[ind]) or
            (sum(relevant) == 2 and row[ind]))


def next_row(row):
    return tuple(get_trap(row, i) for i in range(len(row)))


def count(row, n):
    total = 0
    for _ in range(n):
        total += sum(row)
        row = next_row(row)
    return len(row) * n - total


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert get_trap((False, False, True, True, False), 1)
    assert not get_trap((False, False, True, True, False), 0)
    assert next_row((False, False, True, True, False)) == (False, True, True, True, True)
    assert next_row((False, True, True, True, True)) == (True, True, False, False, True)
    assert count(parse('.^^.^.^^^^'), 10) == 38

    puz = Puzzle(2016, 18)
    row = parse(puz.input_data)

    puz.answer_a = count(row, 40)
    print('Part 1:', puz.answer_a)

    puz.answer_b = count(row, 400000)
    print('Part 2:', puz.answer_b)