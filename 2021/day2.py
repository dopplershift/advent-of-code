def solve(s):
    x = 0
    depth = 0
    aim = 0
    depth2 = 0
    for line in s.split('\n'):
        cmd, d = line.split(' ')
        d = int(d)
        if cmd == 'forward':
            x += d
            depth2 += aim * d
        elif cmd == 'down':
            depth += d
            aim += d
        elif cmd == 'up':
            depth -= d
            aim -= d
    return x * depth, x * depth2


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''

    part1, part2 = solve(sample)
    assert part1 == 150
    assert part2 == 900

    puz = Puzzle(2021, 2)
    part1, part2 = solve(puz.input_data)

    puz.answer_a = part1
    print('Part 1:', puz.answer_a)

    puz.answer_b = part2
    print('Part 2:', puz.answer_b)