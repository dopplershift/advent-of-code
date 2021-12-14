from collections import Counter
import functools


def run(data):
    entries = parse(data)
    return part1(entries), solve(entries)


def parse(s):
    return [tuple(map(lambda s: s.split(' '), line.split(' | '))) for line in s.split('\n')]


def part1(entries):
    return sum(len(item) in {2, 3, 4, 7} for unique, digits in entries for item in digits)


def decode(unique, digits):
    # We really only need to use the full set of patterns to find 1 and 4,
    # which gives the cf and bd pairs.
    for item in unique:
        if len(item) == 2:
            cf = set(item)
        elif len(item) == 4:
            bd = set(item)
    bd -= cf

    # We can just walk through the digits directly and identify them by length
    # and which of cf or bd they have.
    val = 0
    for s in digits:
        l = len(s)
        if l == 2:
            digit = 1
        elif l == 3:
            digit = 7
        elif l == 4:
            digit = 4
        elif l == 5:
            letters = set(s)
            if cf < letters:
                digit = 3
            elif bd < letters:
                digit = 5
            else:
                digit = 2
        elif l == 6:
            letters = set(s)
            if not cf < letters:
                digit = 6
            elif not bd < letters:
                digit = 0
            else:
                digit = 9
        elif l == 7:
            digit = 8
        val = 10 * val + digit

    return val


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

    assert decode(*parse('acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf')[0]) == 5353
    for item, answer in zip(parse(sample), [8394, 9781, 1197, 9361, 4873, 8418, 4548, 1625, 8717, 4315]):
        assert decode(*item) == answer

    test_a, test_b = run(sample)
    assert test_a == 26
    assert test_b == 61229

    puz = Puzzle(2021, 8)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
