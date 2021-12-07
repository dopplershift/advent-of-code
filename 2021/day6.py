def parse(s):
    return list(map(int, s.split(',')))


def age(population, n=80):
    # Only need to count how many fish we have spawning on each day, and grow
    # the population as appropriate.
    grouped = [0] * 7
    ready = aging = 0
    for member in population:
        grouped[member] += 1

    for day in range(n):
        new = grouped[day % 7]
        grouped[day % 7] += ready

        # These two variables account being shifted into each other and eventually
        # included accounts for the two day + one propgation cycle delay before having
        # offspring.
        ready = aging
        aging = new

    return sum(grouped) + ready + aging


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
