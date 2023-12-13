def find_hreflection(pattern):
    # Find horizontal reflection axis
    options = []
    for y, row in enumerate(pattern):
        search_start = 1 if y == 0 else len(pattern) - 1
        while search_start < len(pattern):
            try:
                next_match = pattern[search_start:].index(row) + search_start
                mirror = y + next_match
                if mirror % 2 == 1:
                    for y2 in range(y + 1, next_match):
                        if pattern[y2] != pattern[mirror - y2]:
                            break
                    else:
                        yield mirror // 2 + 1
                search_start = next_match + 1
            except ValueError:
                break


def find_reflection(pattern):
    for row in find_hreflection(pattern):
        if row:
            yield 100 * row

    flipped_pattern = [''.join(row[i] for row in pattern) for i in range(len(pattern[0]))]
    for col in find_hreflection(flipped_pattern):
        if col:
            yield col


def iter_pattern_mods(pattern):
    for y, row in enumerate(pattern):
        for x, c in enumerate(row):
            cp = pattern.copy()
            row_list = list(row)
            row_list[x] = '#' if c == '.' else '.'
            cp[y] = ''.join(row_list)
            yield cp


def part2(patterns):
    total = 0
    for pattern in patterns:
        orig = list(find_reflection(pattern))
        for mod in iter_pattern_mods(pattern):
            done = False
            for ref in find_reflection(mod):
                if ref and ref not in orig:
                    total += ref
                    done = True
                    break
            if done:
                break

    return total


def parse(data):
    return [pattern.split('\n') for pattern in data.split('\n\n')]


def run(data):
    mirrors = parse(data)
    part1 = sum(v for p in mirrors for v in find_reflection(p))
    return part1, part2(mirrors)

if __name__ == '__main__':
    from aocd.models import Puzzle


    t = '''#..####
.##.#..
.##.#.#
#..####
#..####
.##.#.#
.##.#..
#..####
.##...#
#..###.
..###..'''
    test_a, _ = run(t)
    assert test_a == 400


    sample = '''#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#'''

    test_a, test_b = run(sample)
    assert test_a == 405
    assert test_b == 400

    puz = Puzzle(2023, 13)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
