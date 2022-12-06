import string

def duplicate(pack):
    l = len(pack)
    return ''.join(set(pack[:l//2]) & set(pack[l//2:]))


def badge(packs):
    common = set(packs[0])
    for p in packs[1:]:
        common &= set(p)
    return ''.join(common)


def priority(c):
    return ord(c) - 96 if c in string.ascii_lowercase else ord(c) - 38


def run(data):
    packs = data.split('\n')
    groups = iter(packs)
    return sum(priority(duplicate(pack)) for pack in packs), sum(priority(badge(group)) for group in zip(groups, groups, groups))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw'''

    test_a, test_b = run(sample)
    assert test_a == 157
    assert test_b == 70

    puz = Puzzle(2022, 3)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
