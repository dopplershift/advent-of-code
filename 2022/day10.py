timing = {'noop': 1, 'addx': 2}


def execute(prog):
    screen_width = 40
    prog = prog[::-1]
    regx = 1

    signal_strength = 0
    screen = []

    busy = 0
    cycle = 0
    while prog:
        cycle += 1

        if busy:
            busy -= 1
        else:
            busy = timing[prog[-1][0]] - 1

        # Only needed for part1
        if (cycle - 20) % 40 == 0:
            signal_strength += cycle * regx

        screen.append('#' if abs((cycle - 1) % screen_width - regx) <= 1 else '.')

        if not busy:
            cmd = prog.pop()
            if cmd[0] == 'addx':
                regx += cmd[1]

    return signal_strength, '\n'.join(''.join(screen[i*screen_width:(i + 1) * screen_width]) for i in range(6))


def parse(data):
    return [((parts := line.split())[0],) + tuple(map(int, parts[1:])) for line in data.split('\n')]


def run(data):
    prog = parse(data)

    return execute(prog)


if __name__ == '__main__':
    from aoc_tools import ocr
    from aocd.models import Puzzle

    sample = '''addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop'''

    test_a, test_b = run(sample)
    assert test_a == 13140

    assert test_b == '''##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....'''

    puz = Puzzle(2022, 10)
    part_a, part_b = run(puz.input_data)
    part_b = ocr(part_b)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
