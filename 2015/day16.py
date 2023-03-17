def parse(s):
    return [dict(t.split(': ') for t in line.split(': ', maxsplit=1)[-1].split(', '))
            for line in s.splitlines()]


def solve(aunts, machine):
    for num, a in enumerate(aunts, start=1):
        if all(machine[criteria] == int(val) for criteria, val in a.items()):
            return num


def check(aunt, machine):
    for criteria, val in aunt.items():
        if criteria in {'cats', 'trees'}:
            if int(val) <= machine[criteria]:
                return False
        elif criteria in {'pomeranians', 'goldfish'}:
            if int(val) >= machine[criteria]:
                return False
        elif int(val) != machine[criteria]:
            return False
    return True


def solve2(aunts, machine):
    for num, a in enumerate(aunts, start=1):
        if check(a, machine):
            return num


if __name__ == '__main__':
    from aocd.models import Puzzle

    machine = {'children': 3, 'cats': 7, 'samoyeds': 2, 'pomeranians': 3,
            'akitas': 0, 'vizslas': 0, 'goldfish': 5, 'trees': 3,
            'cars': 2, 'perfumes': 1}

    puz = Puzzle(2015, 16)
    aunts = parse(puz.input_data)

    puz.answer_a = solve(aunts, machine)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve2(aunts, machine)
    print(f'Part 2: {puz.answer_b}')
