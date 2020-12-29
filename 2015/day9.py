import itertools


def parse(s):
    table = {}
    for line in s.splitlines():
        line = line.lstrip()
        route, dist = line.split(' = ')
        start, end = route.split(' to ')
        table[start, end] = int(dist)
    return table


def routes(table):
    for route in itertools.permutations({*(k[0] for k in table), *(k[1] for k in table)}):
        yield sum(table.get((start, end), table.get((end, start))) for start, end in zip(route[1:], route[:-1]))


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = r'''London to Dublin = 464
    London to Belfast = 518
    Dublin to Belfast = 141'''

    table = parse(t)
    assert min(routes(table)) == 605
    assert max(routes(table)) == 982

    puz = Puzzle(2015, 9)
    table = parse(puz.input_data)

    puz.answer_a = min(routes(table))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = max(routes(table))
    print(f'Part 2: {puz.answer_b}')