def parse(lines):
    for line in lines:
        yield tuple(map(int, line.split()))


def parse2(lines):
    buf = []
    for line in lines:
        buf.extend(map(int, line.split()))
        if len(buf) == 9:
            yield buf[::3]
            yield buf[1::3]
            yield buf[2::3]
            buf = []


def valid(triangle):
    a, b, c = triangle
    return a + b > c and a + c > b and b + c > a


def solve(text, parser=parse):
    return sum(valid(tri) for tri in parser(text.split('\n')))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert not valid([5, 10, 25])

    lines = '101 301 501\n102 302 502\n103 303 503'.split('\n')
    assert list(parse2(lines)) == [[101, 102, 103], [301, 302, 303], [501, 502, 503]]

    puz = Puzzle(2016, 3)

    puz.answer_a = solve(puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = solve(puz.input_data, parse2)
    print('Part 2:', puz.answer_b)
