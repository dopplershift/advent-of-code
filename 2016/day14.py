from collections import deque
from itertools import count, islice
from hashlib import md5
import heapq
import re

triplet = re.compile(r'(([0-9a-f])\2{2,})', re.ASCII)

def hash_it(i, salt, stretch=0):
    h = md5(salt + str(i).encode('ascii')).hexdigest()
    for _ in range(stretch):
        h = md5(h.encode('ascii')).hexdigest()
    return h


def keys(salt, stretch=0):
    salt = salt.encode('ascii')
    buffer = [deque() for _ in range(16)]
    key_queue = []
    for index in count():
        h = hash_it(index, salt, stretch)
        for num, (tri, *_) in enumerate(re.findall(triplet, h)):
            # Potential closing hash
            matches = buffer[int(tri[0], 16)]
            if len(tri) >= 5:
                while index - matches[0][0] > 1000:
                    matches.popleft()
                for prev_index, key in matches:
                    heapq.heappush(key_queue, (prev_index, key))
            if num == 0:
                matches.append((index, h))
        if key_queue and index - key_queue[0][0] >= 1000:
            yield heapq.heappop(key_queue)


def get_nth_key_index(salt, n, stretch=0):
    return next(islice(keys(salt, stretch), n, None))[0]


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert re.findall(triplet, 'cc38887a5') == [('888', '8')]
    assert get_nth_key_index('abc', 0) == 39
    assert get_nth_key_index('abc', 1) == 92
    assert get_nth_key_index('abc', 63) == 22728

    assert hash_it(0, 'abc'.encode('ascii'), 2016) == 'a107ff634856bb300138cac6568c0f24'
    assert get_nth_key_index('abc', 0, 2016) == 10
    assert get_nth_key_index('abc', 63, 2016) == 22551

    puz = Puzzle(2016, 14)

    puz.answer_a = get_nth_key_index(puz.input_data, 63)
    print('Part 1:', puz.answer_a)

    puz.answer_b = get_nth_key_index(puz.input_data, 63, 2016)
    print('Part 2:', puz.answer_b)
