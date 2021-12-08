from collections import Counter
import functools


def parse(s):
    return [tuple(map(lambda s: s.split(' '), line.split(' | '))) for line in s.split('\n')]


def part1(entries):
    return sum(len(item) in {2, 3, 4, 7} for unique, digits in entries for item in digits)


def identify(unique):
    # By processing by increasing size, we can identify 1 and 4
    # along the way, which gives us the cf and bd segments. These
    # pairs are enough to discern among (2, 3, 5) and (0, 6, 9)
    transform = {}
    for item in sorted(unique, key=lambda i: len(i)):
        letters = set(item)
        ordered = tuple(sorted(item))
        if len(item) == 2:
            transform[ordered] = 1
            cf = letters
        elif len(item) == 3:
            transform[ordered] = 7
        elif len(item) == 4:
            transform[ordered] = 4
            bd = letters - cf
        elif len(item) == 5:
            if cf < letters:
                transform[ordered] = 3
            elif bd < letters:
                transform[ordered] = 5
            else:
                transform[ordered] = 2
        elif len(item) == 6:
            if not (cf < letters):
                transform[ordered] = 6
            elif not (bd < letters):
                transform[ordered] = 0
            else:
                transform[ordered] = 9
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
