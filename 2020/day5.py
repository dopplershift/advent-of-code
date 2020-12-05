import functools

# This was my original implementation
def get_id(s):
    row = 0
    col = 0
    for ind, char in enumerate(s[:7]):
        if char == 'B':
            row |= 2**(6 - ind)
    for ind, char in enumerate(s[7:]):
        if char == 'R':
            col |= 2**(2 - ind)
    return row * 8 + col


# This is equivalent--Multiplying by 8 is the same as shifting left 3 bits
# which is how many L/R characters there are for a row.
def get_id(s):
    # For each character in the string shift what we have left so we can
    # add on the right, setting the bit if we have a character that takes
    # the "upper half"
    return functools.reduce(lambda sid, char: sid<<1 | (char in 'BR'), s, 0)


def find_missing_id(ids):
    ids = sorted(ids)
    return next(filter(lambda i: i[1] - i[0] > 1, zip(ids[:-1], ids[1:])))[0] + 1


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert get_id('FBFBBFFRLR') == 357
    assert get_id('BFFFBBFRRR') == 567
    assert get_id('FFFBBBFRRR') == 119
    assert get_id('BBFFBBFRLL') == 820

    puz = Puzzle(2020, 5)
    ids = [get_id(entry) for entry in puz.input_data.split('\n')]

    puz.answer_a = max(ids)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_missing_id(ids)
    print(f'Part 2: {puz.answer_b}')