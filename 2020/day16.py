from collections import deque


def make_range(s):
    return tuple(map(int, s.split('-')))


def parse(s):
    f, t, n = s.split('\n\n')
    fields = {}
    for line in f.split('\n'):
        name, vals = line.split(': ')
        fields[name] = list(map(make_range, vals.split(' or ')))

    t = t.split('\n')[1]
    ticket = tuple(map(int, t.split(',')))

    nearby = [tuple(map(int, l.split(','))) for l in n.split('\n')[1:]]
    return fields, ticket, nearby


def part1(fields, nearby):
    error_rate = 0
    for t in nearby:
        for v in t:
            if not any(a <= v <= b for entry in fields.values() for (a, b) in entry):
                error_rate += v
    return error_rate


def find_valid(fields, nearby):
    return filter(lambda t: all(any((a1 <= v <= b1 or a2 <= v <= b2)
                                    for ((a1, b1), (a2, b2)) in fields.values())
                                for v in t), nearby)


def decode_ticket(fields, ticket, nearby):
    valid_tickets = list(find_valid(fields, nearby))
    posmap = {}  # Field -> index

    todo = deque(range(len(ticket)))
    while todo:
        ind = todo.pop()
        options = [key for key, ((a1, b1), (a2, b2)) in fields.items()
                   if all((a1 <= t[ind] <= b1 or a2 <= t[ind] <= b2) for t in valid_tickets) and key not in posmap]

        if len(options) > 1:
            todo.appendleft(ind)
        else:
            posmap[options[0]] = ind

    return {key: ticket[posmap[key]] for key in fields}

if __name__ == '__main__':
    import math
    from aocd.models import Puzzle

    t = '''class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12'''

    f, _, n = parse(t)
    assert part1(f, n) == 71
    assert list(find_valid(f, n)) == [(7, 3, 47)]

    t2 = '''class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9'''

    f, t, n = parse(t2)
    assert decode_ticket(f, t, n) == {'class': 12, 'row': 11, 'seat': 13}

    puz = Puzzle(2020, 16)
    fields, ticket, nearby = parse(puz.input_data)

    puz.answer_a = part1(fields, nearby)
    print(f'Part 1: {puz.answer_a}')

    decoded = decode_ticket(fields, ticket, nearby)
    puz.answer_b = math.prod(val for key, val in decoded.items() if key.startswith('departure'))
    print(f'Part 2: {puz.answer_b}')
