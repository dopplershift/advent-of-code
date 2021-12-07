def root(v, mod = 20201227):
    i = 0
    while pow(7, i, mod) != v:
        i += 1
    return i

if __name__ == '__main__':
    from aocd.models import Puzzle

    c = 5764801
    d = 17807724
    i = root(d)
    assert i == 11
    assert root(c) == 8
    assert pow(c, i, 20201227) == 14897079

    puz = Puzzle(2020, 25)
    c, d = map(int, puz.input_data.split('\n'))
    i = root(c)
    puz.answer_a = pow(d, i, 20201227)
    print(f'Part 1: {puz.answer_a}')
