def parse(l):
    init = l[0].split(':')[1].strip()
    rules = dict()
    for line in l[2:]:
        pattern, res = line.strip().split(' => ')
        if res == '#':
            rules[pattern] = res
    return init, rules


def follow_rules(init, rules, generations=20):
    prepended = appended = 0
    buf = init
    #print(buf)
    for _ in range(generations):
        parts = []
        if '....' + buf[0] in rules:
            prepended += 1
            parts.append('#')
        if '...' + buf[:2] in rules:
            prepended += 1
            parts.append('#')
        for i in range(len(buf)):
            if i < 2:
                group = (2 - i) * '.' + buf[:i+3]
            elif i >= len(buf) - 2:
                group = buf[i-2:] + ('..' if i == len(buf) - 1 else '.')
            else:
                group = buf[i-2:i+3]

            parts.append(rules.get(group, '.'))
    #        print(group, '=>', parts[-1])
        if buf[-2:] + '...' in rules:
            appended += 1
            parts.append('#')
        if buf[-1] + '....' in rules:
            appended += 1
            parts.append('#')
        buf = ''.join(parts)
    #    print(buf)    
    return prepended, buf

def score(line, prepended):
    return sum(i for i,m in zip(range(-prepended, len(line)), line) if m=='#')


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''initial state: #..#.#..##......###...###

    ...## => #
    ..#.. => #
    .#... => #
    .#.#. => #
    .#.## => #
    .##.. => #
    .#### => #
    #.#.# => #
    #.### => #
    ##.#. => #
    ##.## => #
    ###.. => #
    ###.# => #
    ####. => #'''.split('\n')

    init, rules = parse(t)

    pre, line = follow_rules(init, rules)
    assert score(line, pre) == 325

    puz = Puzzle(2018, 12)
    init, rules = parse(puz.input_data.split('\n'))

    pre, line = follow_rules(init, rules)
    puz.answer_a = score(line, pre)
    print(f'Part 1: {puz.answer_a}')

    pre, line = follow_rules(init, rules, 1000)
    puz.answer_b = score(line, pre)
    print(f'Part 2: {puz.answer_b}')