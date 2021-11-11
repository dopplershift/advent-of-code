from collections import Counter
from functools import lru_cache
import re
import string

room_pattern = re.compile(r'(?P<name>[a-z-]+)-(?P<sector>\d+)\[(?P<checksum>[a-z]+)\]')

def parser(lines):
    for line in lines:
        yield parse(line)


def parse(s):
    return room_pattern.match(s).groupdict()


def checksum(name):
    c = Counter(name)
    c.pop('-')
    return ''.join(i[0] for i in sorted(c.items(), key=lambda i: (-i[1], i[0]))[:5])


def valid(room):
    return checksum(room['name']) == room['checksum']


_cache = {}
def get_decoder(n):
    shift = n % 26
    decoder = _cache.get(shift)
    if decoder is None:
        source = string.ascii_lowercase
        shifted = ''.join(chr(ord('a') + (ord(c) - ord('a') + shift) % 26) for c in source)
        decoder = str.maketrans(source + '-', shifted + ' ')
        _cache[shift] = decoder
    return decoder


def solve1(rooms):
    return sum(int(room['sector']) for room in rooms)

def solve2(rooms):
    for room in rooms:
        decode = get_decoder(int(room['sector']))
        if 'north' in room['name'].translate(decode):
            return room['sector']


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert valid(parse('aaaaa-bbb-z-y-x-123[abxyz]'))
    assert valid(parse('a-b-c-d-e-f-g-h-987[abcde]'))
    assert valid(parse('not-a-real-room-404[oarel]'))
    assert not valid(parse('totally-real-room-200[decoy]'))
    assert 'qzmt-zixmtkozy-ivhz'.translate(get_decoder(343)) == 'very encrypted name'

    puz = Puzzle(2016, 4)

    rooms = [room for room in parser(puz.input_data.split('\n')) if valid(room)]
    puz.answer_a = solve1(rooms)
    print('Part 1:', puz.answer_a)

    puz.answer_b = solve2(rooms)
    print('Part 2:', puz.answer_b)