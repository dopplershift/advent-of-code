from hashlib import md5
from itertools import count

def search_hashes(door_id):
    fmt = door_id.encode('ascii') + b'%d'
    for i in count(0):
        digest = md5(fmt % i).hexdigest()
        if digest.startswith('00000'):
            yield digest
    

def crack(door_id):
    pw = ''
    hashes = search_hashes(door_id)
    while len(pw) < 8:
        pw += next(hashes)[5]
    return pw


def crack2(door_id):
    pw = list('-' * 8)
    for digest in search_hashes(door_id):
        if (index := int(digest[5], base=16)) < 8 and pw[index] == '-':
            pw[index] = digest[6]
            if '-' not in pw:
                return ''.join(pw)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert crack('abc') == '18f47a30'
    assert crack2('abc') == '05ace8e3'

    puz = Puzzle(2016, 5)

    puz.answer_a = crack(puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = crack2(puz.input_data)
    print('Part 2:', puz.answer_b)