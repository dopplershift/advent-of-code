from collections import Counter
import functools


def parse(s):
    return [tuple(map(lambda s: s.split(' '), line.split(' | '))) for line in s.split('\n')]


def part1(entries):
    return sum(len(item) in {2, 3, 4, 7} for unique, digits in entries for item in digits)


def identify(unique):
    # Using the number of times each segment appears across
    # each of the ten digits, we can identify segments well
    # enough to discern the digits
    counts = Counter(''.join(unique))
    dg = set()
    for letter, num in counts.items():
        if num == 4:
            e = letter
        elif num == 6:
            b = letter
        elif num == 7:
            dg.add(letter)

    # Using the number of segments for each digit, combined
    # with knowing the true identity of a few key segments allows us to create
    # a mapping of segments (in order) to the correct digit
    transform = {}
    for item in unique:
        ordered = tuple(sorted(item))
        if len(item) == 2:
            transform[ordered] = 1
        elif len(item) == 3:
            transform[ordered] = 7
        elif len(item) == 4:
            transform[ordered] = 4
        elif len(item) == 5:
            if b in item:
                transform[ordered] = 5
            elif e in item:
                transform[ordered] = 2
            else:
                transform[ordered] = 3
        elif len(item) == 6:
            if e not in item:
                transform[ordered] = 9
            elif dg < set(ordered):
                transform[ordered] = 6
            else:
                transform[ordered] = 0
        elif len(item) == 7:
            transform[ordered] = 8

    return transform


def decode(unique, digits):
    mapping = identify(unique)
    return functools.reduce(lambda x, y: 10 * x + mapping[tuple(sorted(y))], digits, 0)


def solve(entries):
    return sum(decode(unique, digits) for unique, digits in entries)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce'''

    entries = parse(sample)
    assert part1(entries) == 26
    assert decode(*parse('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf')[0]) == 5353
    for item, answer in zip(entries, [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]):
        assert decode(*item) == answer
    assert solve(entries) == 61229

    puz = Puzzle(2021, 8)
    entries = parse(puz.input_data)

    puz.answer_a = part1(entries)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = solve(entries)
    print(f'Part 2: {puz.answer_b}')