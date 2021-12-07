def parse(s):
    for line in s.split('\n'):
        rng, c, pw = line.split()
        low, high = map(int, rng.split('-'))
        c = c.rstrip(':')
        yield pw, low, high, c

def valid(pw, low, high, c):
    return low <= pw.count(c) <= high

def valid_new(pw, ind1, ind2, c):
    spot1 = pw[ind1 - 1] == c
    spot2 = pw[ind2 - 1] == c
    return spot1 ^ spot2

if __name__ == '__main__':
    from aocd.models import Puzzle

    test_input = """1-3 a: abcde
    1-3 b: cdefg
    2-9 c: ccccccccc"""

    data = list(parse(test_input))

    # Part 1
    assert valid('abcde', 1, 3, 'a')
    assert not valid('cdefg', 1, 3, 'b')
    assert valid('ccccccccc', 2, 9, 'c')
    assert sum(valid(*i) for i in data) == 2

    # Part 2
    assert valid_new('abcde', 1, 3, 'a')
    assert not valid_new('cdefg', 1, 3, 'b')
    assert not valid_new('ccccccccc', 2, 9, 'c')
    assert sum(valid_new(*i) for i in data) == 1

    puz = Puzzle(2020, 2)
    data = list(parse(puz.input_data))

    puz.answer_a = sum(valid(*i) for i in data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = sum(valid_new(*i) for i in data)
    print('Part 2:', puz.answer_b)
