from hashlib import md5


def find_hash(prefix, key):
    key = key.encode('ascii')
    i = 0
    while True:
        h = md5(key + str(i).encode('ascii')).hexdigest()
        if h.startswith(prefix):
            break
        i += 1
    return i


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert find_hash('00000', 'abcdef') == 609043
    assert find_hash('00000', 'pqrstuv') == 1048970

    puz = Puzzle(2015, 4)
    puz.answer_a = find_hash('00000', puz.input_data.strip())
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_hash('000000', puz.input_data.strip())
    print(f'Part 2: {puz.answer_b}')
