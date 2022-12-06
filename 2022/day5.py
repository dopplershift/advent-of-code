def parse(s):
    crates = dict()
    moves = []
    for line in s.split('\n'):
        if '[' in line:
            for ind, loc in enumerate(range(1, len(line), 4), 1):
                if line[loc] != ' ':
                    crates.setdefault(ind, []).append(line[loc])
        elif 'move' in line:
            moves.append(tuple(map(int, line.split(' ')[1::2])))
    return {i: crates[i][::-1] for i in crates}, moves


def execute_stacks(stacks, moves):
    for num, src, dest in moves:
        for _ in range(num):
            stacks[dest].append(stacks[src].pop())


def execute_seq(crates, moves):
    for num, src, dest in moves:
        crates[dest].extend(crates[src][-num:])
        crates[src] = crates[src][:-num]


def run(data):
    crates, moves = parse(data)
    execute_stacks(crates, moves)

    crates2, moves = parse(data)
    execute_seq(crates2, moves)

    return ''.join(crates[i][-1] for i in sorted(crates)), ''.join(crates2[i][-1] for i in sorted(crates2))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2'''

    test_a, test_b = run(sample)
    assert test_a == 'CMZ'
    assert test_b == 'MCD'

    puz = Puzzle(2022, 5)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
