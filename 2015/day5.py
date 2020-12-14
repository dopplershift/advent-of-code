import re


pat11 = re.compile(r'(.*[aeiou].*){3,}?')
pat12 = re.compile(r'([a-z])\1')
pat13 = re.compile(r'ab|cd|pq|xy')

pat21 = re.compile(r'([a-z]{2}).*\1')
pat22 = re.compile(r'([a-z]).\1')


def nice1(s):
    c1 = pat11.search(s)
    c2 = pat12.search(s)
    c3 = pat13.search(s)
    return c1 is not None and c2 is not None and c3 is None


def nice2(s):
    return pat21.search(s) is not None and pat22.search(s) is not None


def part1(s):
    return sum(nice1(l) for l in s.split('\n'))


def part2(s):
    return sum(nice2(l) for l in s.split('\n'))

if __name__ == '__main__':
    from aocd.models import Puzzle

    assert nice1('ugknbfddgicrmopn')
    assert nice1('aaa')
    assert not nice1('jchzalrnumimnmhp')
    assert not nice1('haegwjzuvuyypxyu')
    assert not nice1('dvszwmarrgswjxmb')

    assert nice2('qjhvhtzxzqqjkmpb')
    assert nice2('xxyxx')
    assert not nice2('uurcxstgmygtbstg')
    assert not nice2('ieodomkazucvgmuy')

    puz = Puzzle(2015, 5)

    puz.answer_a = part1(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(puz.input_data)
    print(f'Part 2: {puz.answer_b}')