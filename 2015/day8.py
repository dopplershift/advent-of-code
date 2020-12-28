def parsed(s):
    it = iter(s)
    while n := next(it, None):
        if n == '\\':
            n = next(it, None)
            if n == 'x':
                yield chr(int(next(it) + next(it), 16))
            else:
                yield n
        else:
            yield n


def quoted(s):
    l = ['"']
    for c in s:
        if c == '"':
            l.append(r'\"')
        elif c == '\\':
            l.append('\\\\')
        else:
            l.append(c)
    l.append('"')
    return ''.join(l)


def part1(s):
    total = 0
    code = 0
    for line in s.split('\n'):
        total += len(line)
        code += len(''.join(parsed(line[1:-1])))
    return total - code


def part2(s):
    total = 0
    code = 0
    for line in s.split('\n'):
        total += len(line)
        code += len(quoted(line))
    return code - total


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = r'''""
    "abc"
    "aaa\"aaa"
    "\x27"'''

    assert part1(t) == 12
    assert part2(t) == 19

    puz = Puzzle(2015, 8)

    puz.answer_a = part1(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(puz.input_data)
    print(f'Part 2: {puz.answer_b}')