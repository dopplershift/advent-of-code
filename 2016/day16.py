def dragon(s):
    return s + '0' + ''.join('0' if c == '1' else '1' for c in reversed(s))


def checksum(s):
    while len(s) % 2 == 0:
        s = ''.join('1' if a==b else '0' for a, b in zip(s[:-1:2], s[1::2]))
    return s


def fill(start, n):
    while len(start) < n:
        start = dragon(start)
    return start[:n]


def solve(inp, n):
    return checksum(fill(inp, n))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert dragon('1') == '100'
    assert dragon('0') == '001'
    assert dragon('11111') == '11111000000'
    assert dragon('111100001010') == '1111000010100101011110000'

    assert checksum('110010110100') == '100'

    assert solve('10000', 20) == '01100'

    puz = Puzzle(2016, 16)

    puz.answer_a = solve(puz.input_data, 272)
    print('Part 1:', puz.answer_a)

    puz.answer_b = solve(puz.input_data, 35651584)
    print('Part 2:', puz.answer_b)