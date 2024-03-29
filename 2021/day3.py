def run(data):
    return power_consumption(data), life_support_rating(data)


def common_bit(bits):
    return '1' if bits.count('1') >= len(bits) / 2 else '0'


def most_common_bits(entries):
    return [common_bit(pos) for pos in zip(*entries)]


def power_consumption(s):
    gamma = ''.join(most_common_bits(s.split('\n')))
    epsilon = ''.join('0' if c == '1' else '1' for c in gamma)
    return int(gamma, 2) * int(epsilon, 2)


def life_support_rating(s):
    total = 1
    for op in (str.__eq__, str.__ne__):
        rating = s.split('\n')
        for pos in range(len(rating[0])):
            if len(rating) == 1:
                break
            bit = common_bit([item[pos] for item in rating])
            rating = [item for item in rating if op(item[pos], bit)]
        total *= int(rating[0], 2)
    return total


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''

    test_a, test_b = run(sample)
    assert test_a == 198
    assert test_b == 230

    puz = Puzzle(2021, 3)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
