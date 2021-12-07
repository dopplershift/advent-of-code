def get_houses(dirs):
    x, y = 0, 0
    houses = {(x, y)}
    for d in dirs:
        if d == '>':
            x += 1
        elif d == '<':
            x -= 1
        elif d == '^':
            y += 1
        elif d == 'v':
            y -= 1
        houses.add((x, y))
    return houses


def part1(s):
    return len(get_houses(s))


def part2(s):
    return len(get_houses(s[::2]) | get_houses(s[1::2]))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert part1('>') == 2
    assert part1('^>v<') == 4
    assert part1('^v^v^v^v^v') == 2

    assert part2('^v') == 3
    assert part2('^>v<') == 3
    assert part2('^v^v^v^v^v') == 11

    puz = Puzzle(2015, 3)

    puz.answer_a = part1(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(puz.input_data)
    print(f'Part 2: {puz.answer_b}')
