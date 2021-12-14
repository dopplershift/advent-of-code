def run(data):
    start, end = map(int, data.split('-'))
    part_a = sum(is_valid(str(i)) for i in range(start, end + 1))
    part_b = sum(is_valid2(str(i)) for i in range(start, end + 1))
    return part_a, part_b


def is_valid(pwd):
    has_pair = False
    for i,j in zip(pwd[:-1], pwd[1:]):
        if j<i:
            return False
        has_pair |= (j == i)
    return has_pair


def is_valid2(pwd):
    has_pair = False
    for i in range(len(pwd) - 1):
        if pwd[i + 1]<pwd[i]:
            return False
        test_val = (pwd[i] == pwd[i + 1])
        if i > 0:
            test_val &= pwd[i - 1] != pwd[i]
        if i < len(pwd) - 2:
            test_val &= (pwd[i + 1] != pwd[i + 2])
        has_pair |= test_val
    return has_pair


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert is_valid('111111')
    assert not is_valid('223450')
    assert not is_valid('123789')

    assert is_valid2('112233')
    assert not is_valid2('123444')
    assert is_valid2('111122')

    puz = Puzzle(2019, 4)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
