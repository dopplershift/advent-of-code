from collections import deque


def parse(s):
    return list(map(int, s.split(',')))


def age(population, n=80):
    grouped = [0] * 7
    new = [0] * 7
    for member in population:
        grouped[member] += 1

    for day in range(n):
        new[(day + 2) % 7] = grouped[day % 7]
        grouped[day % 7] += new[day % 7]
        new[day % 7] = 0
    
    return sum(grouped) + sum(new)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''3,4,3,1,2'''

    pop = parse(sample)
    assert age(pop, 18) == 26
    assert age(pop, 80) == 5934
    assert age(pop, 256) == 26984457539

    puz = Puzzle(2021, 6)
    pop = parse(puz.input_data)

    puz.answer_a = age(pop, 80)
    print('Part 1:', puz.answer_a)

    puz.answer_b = age(pop, 256)
    print('Part 2:', puz.answer_b)