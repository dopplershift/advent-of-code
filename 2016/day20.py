from itertools import chain


def parse(s):
    for line in s.split('\n'):
        yield tuple(map(int, line.split('-')))

def merge(ranges):
    ranges = sorted(ranges)
    merged = []
    cur_start, cur_end = ranges[0]
    for s, e in ranges[1:]:
        #print(s, e)
        if s <= cur_end + 1:
            cur_end = max(cur_end, e)
        else:
            merged.append((cur_start, cur_end))
            cur_start, cur_end = s, e
    return merged + [(cur_start, cur_end)]


def first_avail(ranges):
    return min(ranges)[-1] + 1


def num_avail(ranges, min_ip, max_ip):
    starts, ends = zip(*ranges)
    return sum(s - e - 1 for s, e in zip(chain(starts, [max_ip + 1]), chain([min_ip - 1], ends)))

if __name__ == '__main__':
    from aocd.models import Puzzle


    s = '''5-8
    0-2
    4-7'''
    r = merge(parse(s))
    assert r == [(0, 2), (4, 8)]
    assert first_avail(r) == 3
    assert num_avail(r, 0, 9) == 2

    puz = Puzzle(2016, 20)
    ranges = merge(parse(puz.input_data))

    ip = first_avail(ranges)
    for s, e in ranges:
        assert not s < ip < e
    for s, e in parse(puz.input_data):
        assert not s < ip < e

    puz.answer_a = ip
    print('Part 1:', puz.answer_a)

    puz.answer_b = num_avail(ranges, 0, 4294967295)
    print('Part 2:', puz.answer_b)