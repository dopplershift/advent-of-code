from functools import lru_cache

def parse(s):
    return dict(line.split(' -> ')[::-1] for line in s.split('\n'))


@lru_cache
def walk(end):
    try:
        return int(end)
    except ValueError:
        command = w[end]

    if 'AND' in command:
        a, b = command.split(' AND ')
        return walk(a) & walk(b)
    elif 'OR' in command:
        a, b = command.split(' OR ')
        return walk(a) | walk(b)
    elif 'LSHIFT' in command:
        a, b = command.split(' LSHIFT ')
        return walk(a) << int(b)
    elif 'RSHIFT' in command:
        a, b = command.split(' RSHIFT ')
        return walk(a) >> int(b)
    elif 'NOT' in command:
        return ~walk(command[4:]) & 0xFFFF
    else:
        return walk(command)


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''123 -> x
    456 -> y
    x AND y -> d
    x OR y -> e
    x LSHIFT 2 -> f
    y RSHIFT 2 -> g
    NOT x -> h
    NOT y -> i'''

    wires = parse(t)

    puz = Puzzle(2015, 7)

    w = parse(puz.input_data)
    res = walk('a')

    puz.answer_a = res
    print(f'Part 1: {puz.answer_a}')

    w['b'] = str(res)
    walk.cache_clear()
    puz.answer_b = walk('a')
    print(f'Part 2: {puz.answer_b}')
