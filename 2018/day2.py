from collections import Counter
import itertools


def checksum(ids):
    twos = 0
    threes = 0
    for box in ids:
        counts = Counter(box)
        if 2 in counts.values():
            twos += 1
        if 3 in counts.values():
            threes += 1
    return twos * threes


def find_boxes(ids):
    for box1, box2 in itertools.combinations(ids, 2):
        diff = [i==j for i,j in zip(box1, box2)]
        if sum(diff) == (len(box1) - 1):
            ind = diff.index(False)
            return box1[:ind] + box1[ind+1:]

if __name__ == '__main__':
    from aocd.models import Puzzle

    assert checksum(['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']) == 12

    assert find_boxes(['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxy']) == 'fgij'

    puz = Puzzle(2018, 2)
    boxes = puz.input_data.split('\n')

    puz.answer_a = checksum(boxes)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_boxes(boxes)
    print(f'Part 2: {puz.answer_b}')