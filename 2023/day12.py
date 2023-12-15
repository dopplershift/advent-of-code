import functools


def unfold(listing, groups, n=5):
    return '?'.join([listing] * n), groups * n


@functools.cache
def count(listing, groups):
    if not groups:
        return int('#' not in listing)

    if not listing:
        return 0

    if listing[0] == '?':
        return count('.' + listing[1:], groups) + count('#' + listing[1:], groups)

    block_len = 1
    for c in listing[1:]:
        if c == listing[0]:
            block_len += 1
        else:
            break

    rest = listing[block_len:]
    if listing[0] == '.':
        return count(rest, groups)
    elif listing[0] == '#':
        if block_len == groups[0]:
            groups = groups[1:]
            if rest and rest[0] == '?':
                rest = '.' + rest[1:]
            return count(rest, groups)
        elif rest and rest[0] == '?':
            return count(listing[:block_len] + '#' + rest[1:], groups)

    return 0


def parse(data):
    for line in data.split('\n'):
        listing, s = line.split()
        groups = tuple(map(int, s.split(',')))
        yield listing, groups


def run(data):
    part1 = sum(count(listing, groups) for listing, groups in parse(data))
    part2 = sum(count(*unfold(listing, groups)) for listing, groups in parse(data))
    return part1, part2


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert count('???.###', (1, 1, 3)) == 1
    assert count('.??..??...?##.', (1, 1, 3)) == 4
    assert count('?#?#?#?#?#?#?#?', (1, 3, 1, 6)) == 1
    assert count('????.#...#...', (4, 1, 1)) == 1
    assert count('????.######..#####.', (1, 6, 5)) == 4
    assert count('?###????????', (3, 2, 1)) == 10
    assert count('??#.#???#?', (2, 1, 1)) == 1

    assert count(*unfold('???.###', (1, 1, 3))) == 1
    assert count(*unfold('.??..??...?##.', (1, 1, 3))) == 16384
    assert count(*unfold('?#?#?#?#?#?#?#?', (1, 3, 1, 6))) == 1
    assert count(*unfold('????.#...#...', (4, 1, 1))) == 16
    assert count(*unfold('????.######..#####.', (1, 6, 5))) == 2500
    assert count(*unfold('?###????????', (3, 2, 1))) == 506250

    sample = '''???.### 1,1,3
    .??..??...?##. 1,1,3
    ?#?#?#?#?#?#?#? 1,3,1,6
    ????.#...#... 4,1,1
    ????.######..#####. 1,6,5
    ?###???????? 3,2,1'''

    test_a, test_b = run(sample)
    assert test_a == 21
    assert test_b == 525152

    puz = Puzzle(2023, 12)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
