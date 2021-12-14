def solve(s):
    x = 0
    aim = 0
    depth = 0
    for line in s.split('\n'):
        cmd, d = line.split(' ')
        d = int(d)
        match cmd:
            case 'forward':
                x += d
                depth += aim * d
            case 'down':
                aim += d
            case 'up':
                aim -= d
    return x * aim, x * depth


run = solve


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
