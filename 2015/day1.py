def part1(s):
    return sum(1 if c == '(' else -1 for c in s.strip())


def part2(s):
    floor = 0
    for pos, c in enumerate(s.strip()):
        floor += 1 if c == '(' else -1
        if floor < 0:
            break
    return pos + 1


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert part1('(())') == 0
    assert part1('))(((((') == 3
    assert part1(')())())') == -3

    assert part2('()())') == 5

    puz = Puzzle(2015, 1)

    puz.answer_a = part1(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(puz.input_data)
    print(f'Part 2: {puz.answer_b}')
