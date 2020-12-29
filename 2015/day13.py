import itertools


def pairwise_circular(c):
    a,b = itertools.tee(c)
    return zip(a, itertools.chain(b, [next(b, None)]))


def parse(s):
    rules = dict()
    for line in s.splitlines():
        name, _, which, val, *_, name2 = line.split()
        rules[name, name2[:-1]] = int(val) * (-1 if which == 'lose' else 1)
    return rules


def arrange(rules, include_self=False):
    names = {k[0] for k in rules}
    if include_self:
        names.add('me')
    return max(sum(rules.get(p, 0) + rules.get(p[::-1], 0)
                   for p in pairwise_circular(order))
               for order in itertools.permutations(names, len(names)))


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''Alice would gain 54 happiness units by sitting next to Bob.
    Alice would lose 79 happiness units by sitting next to Carol.
    Alice would lose 2 happiness units by sitting next to David.
    Bob would gain 83 happiness units by sitting next to Alice.
    Bob would lose 7 happiness units by sitting next to Carol.
    Bob would lose 63 happiness units by sitting next to David.
    Carol would lose 62 happiness units by sitting next to Alice.
    Carol would gain 60 happiness units by sitting next to Bob.
    Carol would gain 55 happiness units by sitting next to David.
    David would gain 46 happiness units by sitting next to Alice.
    David would lose 7 happiness units by sitting next to Bob.
    David would gain 41 happiness units by sitting next to Carol.'''

    r = parse(t)
    assert arrange(r) == 330

    puz = Puzzle(2015, 13)

    puz.answer_a = arrange(parse(puz.input_data))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = arrange(parse(puz.input_data), True)
    print(f'Part 2: {puz.answer_b}')