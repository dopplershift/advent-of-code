from collections import Counter


def run(data):
    template, rules = parse(data)
    return grow(template, rules, 10), grow(template, rules, 40)


def parse(s):
    template, rules = s.split('\n\n')
    rules = dict(line.split(' -> ') for line in rules.split('\n'))
    return template, rules


def grow(poly, rules, n):
    counts = Counter(map(str.__add__, poly, poly[1:]))
    for _ in range(n):
        new_counts = Counter()
        for pair, num in counts.items():
            match = rules[pair]
            new_counts[pair[0] + match] += num
            new_counts[match + pair[1]] += num
        counts = new_counts

    # Since every pair overlaps, we only count the left element of
    # every pair--BUT need to add the last element since it's not otherwise
    # counted. Also, the last character remains constant.
    element_counts = Counter(poly[-1:])
    for item, val in counts.items():
        element_counts[item[0]] += val
    common = element_counts.most_common()
    return common[0][-1] - common[-1][-1]


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C'''

    test_a, test_b = run(sample)
    assert test_a == 1588
    assert test_b == 2188189693529

    puz = Puzzle(2021, 14)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
