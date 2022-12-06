def run(data):
    totals = sorted(sum(map(int, elf.split('\n'))) for elf in data.split('\n\n'))
    return totals[-1], sum(totals[-3:])


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''1000
2000
3000

4000

5000
6000

7000
8000
9000

10000'''

    test_a, test_b = run(sample)
    assert test_a == 24000
    assert test_b == 45000

    puz = Puzzle(2022, 1)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
