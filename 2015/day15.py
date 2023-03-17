from functools import reduce

def parse(s):
    return [tuple(int(item.split()[-1]) for item in line.split(':')[-1].split(','))
            for line in s.splitlines()]


def options(budget, n):
    if n == 1:
        yield (budget,)
    else:
        for i in range(budget + 1):
            for opts in options(budget - i, n - 1):
                yield (i,) + opts


def score(ingreds, amounts):
    return reduce(lambda x, y: max(x, 0) * y,
        (sum(amt * rating for amt, rating in zip(amounts, (i[ind] for i in ingreds))) for ind in range(len(ingreds[0]) - 1)))


def solve(ingreds):
    return max(score(ingreds, amounts)
            for amounts in options(100, len(ingreds)))


def solve2(ingreds):
    return max(score(ingreds, amounts)
            for amounts in options(100, len(ingreds))
            if sum(a * i[-1] for a, i in zip(amounts, ingreds)) == 500)


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3'''

    assert solve(parse(t)) == 62842880
    assert solve2(parse(t)) == 57600000

    puz = Puzzle(2015, 15)
    ingreds = parse(puz.input_data)

    puz.answer_a = solve(ingreds)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve2(ingreds)
    print(f'Part 2: {puz.answer_b}')
