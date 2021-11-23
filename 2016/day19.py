def collapse(n):
    elves = list(range(1, n + 1))
    while len(elves) > 1:
        odd = len(elves) % 2
        elves = elves[::2]
        if odd:
            elves.pop(0)
    return elves[0]


def calc(n):
    p = 1
    while p < n:
        p *= 2
    return 2 * (n % (p // 2)) + 1


def collapse_across(n):
    ind = 0
    elves = list(range(1, n + 1))
    while len(elves) > 1:
        stolen = (ind + len(elves) // 2) % len(elves)
        elves.pop(stolen)
        ind += (1 - (stolen < ind))
        if ind >= len(elves):
            ind = 0
    return elves[0]


def calc_across(n):
    p = 1
    while p < n:
        p *= 3
    m = p // 3
    return (n // (2 * m) + 2 * (n // (3 * m))) * m + (n // m) * (n % m)


if __name__ == '__main__':
    from aocd.models import Puzzle
    puz = Puzzle(2016, 19)

    assert collapse(5) == 3

    assert collapse_across(2) == 1
    assert collapse_across(3) == 3
    assert collapse_across(4) == 1
    assert collapse_across(5) == 2
    assert collapse_across(6) == 3
    assert collapse_across(7) == 5
    assert collapse_across(8) == 7
    assert collapse_across(9) == 9
    assert collapse_across(10) == 1

    for i in range(2, 1000):
        if collapse(i) != calc(i):
            print('next:', i)
        if collapse_across(i) != calc_across(i):
            print('across:', i)

    puz.answer_a = calc(int(puz.input_data))
    print('Part 1:', puz.answer_a)

    puz.answer_b = calc_across(int(puz.input_data))
    print('Part 2:', puz.answer_b)