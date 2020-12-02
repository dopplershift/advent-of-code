def shuffle(cards, cmds):
    cards = list(cards)
    for cmd in cmds:
        if cmd.startswith('cut'):
            _, n = cmd.split()
            n = int(n)
            cards = cards[n:] + cards[:n]
        elif cmd.strip() == 'deal into new stack':
            cards = cards[::-1]
        elif cmd.startswith('deal with increment'):
            *_, n = cmd.split()
            n = int(n)
            newcards = [-1] * len(cards)
            for i, c in enumerate(cards):
                newcards[(i * n) % len(cards)] = c
            cards = newcards
    return cards


def inv_shuffle_funcs(l, cmds):
    for cmd in reversed(cmds):
        if cmd.startswith('cut'):
            n = int(cmd.split()[-1])
            yield lambda p, n=n, l=l: (p + n) % l
        elif cmd.strip() == 'deal into new stack':
            yield lambda p, l=l: (l - p - 1) % l
        elif cmd.startswith('deal with increment'):
            n = int(cmd.split()[-1])
            def lam(p, n=n, l=l):
                for m in range(l):
                    if not (p + m * l) % n:
                        return (p + m * l) // n
            yield lam


def inv_shuffle(pos, funcs):
    for f in funcs:
#         print(pos, end=' -> ')
        pos = f(pos)
#         print(pos)
    return pos


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert shuffle(range(10), ['deal into new stack']) == [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    assert shuffle(range(10), ['cut 3']) == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    assert shuffle(range(10), ['cut -4']) == [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
    assert shuffle(range(10), ['deal with increment 3']) == [0, 7, 4, 1, 8, 5, 2, 9, 6, 3]
    assert shuffle(range(10), ['deal with increment 7',
                               'deal into new stack',
                               'deal into new stack']) == [
        0, 3, 6, 9, 2, 5, 8, 1, 4, 7]

    assert shuffle(range(10), ['cut 6', 'deal with increment 7',
                               'deal into new stack']) == [
        3, 0, 7, 4, 1, 8, 5, 2, 9, 6]

    assert shuffle(range(10), ['deal with increment 7',
                               'deal with increment 9',
                               'cut -2',]) == [
        6, 3, 0, 7, 4, 1, 8, 5, 2, 9]

    assert shuffle(range(10), ['deal into new stack',
                               'cut -2',
                               'deal with increment 7',
                               'cut 8',
                               'cut -4',
                               'deal with increment 7',
                               'cut 3',
                               'deal with increment 9',
                               'deal with increment 3',
                               'cut -1']) == [
        9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

    # Tests for part 2
    f = list(inv_shuffle_funcs(10, ['deal into new stack']))
    assert inv_shuffle(0, f) == 9
    assert inv_shuffle(2, f) == 7
    assert inv_shuffle(7, f) == 2
    assert inv_shuffle(9, f) == 0

    f = list(inv_shuffle_funcs(10, ['cut 3']))
    assert inv_shuffle(9, f) == 2
    assert inv_shuffle(0, f) == 3

    f = list(inv_shuffle_funcs(10, ['cut -4']))
    assert inv_shuffle(0, f) == 6
    assert inv_shuffle(4, f) == 0
    assert inv_shuffle(9, f) == 5

    f = list(inv_shuffle_funcs(10, ['deal with increment 3']))
    assert inv_shuffle(0, f) == 0
    assert inv_shuffle(4, f) == 8
    assert inv_shuffle(2, f) == 4

    f = list(inv_shuffle_funcs(10, ['deal with increment 9']))
    assert inv_shuffle(0, f) == 0
    assert inv_shuffle(9, f) == 1

    f = list(inv_shuffle_funcs(10, ['deal into new stack',
                               'cut -2',
                               'deal with increment 7',
                               'cut 8',
                               'cut -4',
                               'deal with increment 7',
                               'cut 3',
                               'deal with increment 9',
                               'deal with increment 3',
                               'cut -1']))
    assert inv_shuffle(7, f) == 0
    assert inv_shuffle(9, f) == 6
    assert inv_shuffle(3, f) == 8

    puz = Puzzle(2019, 22)

    cards = shuffle(range(10007), puz.input_data.split('\n'))
    puz.answer_a = cards.index(2019)
    print(f'Part 1: {puz.answer_a}')

    l = 119315717514047
    funcs = list(inv_shuffle_funcs(l, puz.input_data.split('\n')))

    x = 2020
    y = inv_shuffle(x, funcs)
    z = inv_shuffle(y, funcs)

    a = ((y - z) * pow(x - y, l - 2, l)) % l
    b = y - a * x

    n = 101741582076661

    v = (pow(a, n, l) * x + (pow(a, n, l) - 1) * pow(a - 1, l - 2, l) * b) % l
    puz.answer_b = v
    print(f'Part 2: {puz.answer_b}')