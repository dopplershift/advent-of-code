def scrambler(s, ops):
    s = list(s)
    for line in ops.split('\n'):
        command, *rest = line.split(' ')
        if command == 'swap':
            if rest[0] == 'position':
                ind1 = int(rest[1])
                ind2 = int(rest[4])
            else:
                ind1 = s.index(rest[1])
                ind2 = s.index(rest[4])
            s[ind1], s[ind2] = s[ind2], s[ind1]
        elif command == 'rotate':
            if rest[-1].startswith('step'):
                mul = {'left': 1, 'right': -1}[rest[0]]
                n = mul * int(rest[1])
                s = s[n:] + s[:n]
            else:
                ind = s.index(rest[-1])
                s = s[-1:] + s[:-1]
                s = s[-ind:] + s[:-ind]
                if ind >= 4:
                    s = s[-1:] + s[:-1]
        elif command == 'reverse':
            ind1 = int(rest[1])
            ind2 = int(rest[3])
            s[ind1:ind2 + 1] = reversed(s[ind1:ind2 + 1])
        elif command == 'move':
            ind1 = int(rest[1])
            ind2 = int(rest[4])
            s.insert(ind2, s.pop(ind1))
        else:
            raise RuntimeError(f'Unknown command {command}')

    return ''.join(s)


def descrambler(s, ops):
    s = list(s)
    rev_ind_lookup = {((1 + 2 * i + 1 * (i >= 4)) % len(s)): i for i in range(len(s))}
    for line in reversed(ops.split('\n')):
        command, *rest = line.split(' ')
        if command == 'swap':
            if rest[0] == 'position':
                ind1 = int(rest[1])
                ind2 = int(rest[4])
            else:
                ind1 = s.index(rest[1])
                ind2 = s.index(rest[4])
            s[ind1], s[ind2] = s[ind2], s[ind1]
        elif command == 'rotate':
            if rest[-1].startswith('step'):
                mul = {'left': -1, 'right': 1}[rest[0]]
                n = mul * int(rest[1])
                s = s[n:] + s[:n]
            else:
                ind = rev_ind_lookup[s.index(rest[-1])]
                if ind >= 4:
                    s = s[1:] + s[:1]
                s = s[ind:] + s[:ind]
                s = s[1:] + s[:1]
        elif command == 'reverse':
            ind1 = int(rest[1])
            ind2 = int(rest[3])
            s[ind1:ind2 + 1] = reversed(s[ind1:ind2 + 1])
        elif command == 'move':
            ind1 = int(rest[4])
            ind2 = int(rest[1])
            s.insert(ind2, s.pop(ind1))
        else:
            raise RuntimeError(f'Unknown command {command}')

    return ''.join(s)


if __name__ == '__main__':
    assert scrambler('abcde', 'swap position 4 with position 0') == 'ebcda'
    assert scrambler('ebcda', 'swap letter d with letter b') == 'edcba'
    assert scrambler('edcba', 'reverse positions 0 through 4') == 'abcde'
    assert scrambler('abcde', 'rotate left 1 step') == 'bcdea'
    assert scrambler('abcd', 'rotate right 1 step') == 'dabc'
    assert scrambler('bcdea', 'move position 1 to position 4') == 'bdeac'
    assert scrambler('bdeac', 'move position 3 to position 0') == 'abdec'
    assert scrambler('abdec', 'rotate based on position of letter b') == 'ecabd'
    assert scrambler('ecabd', 'rotate based on position of letter d') == 'decab'

    assert descrambler('ebcda', 'swap position 4 with position 0') == 'abcde'
    assert descrambler('edcba', 'swap letter d with letter b') == 'ebcda'
    assert descrambler('abcde', 'reverse positions 0 through 4') == 'edcba'
    assert descrambler('bcdea', 'rotate left 1 step') == 'abcde'
    assert descrambler('dabc', 'rotate right 1 step') == 'abcd'
    assert descrambler('bdeac', 'move position 1 to position 4') == 'bcdea'
    assert descrambler('abdec', 'move position 3 to position 0') == 'bdeac'
    assert descrambler('ecabd', 'rotate based on position of letter b') == 'abdec'
    assert descrambler('decab', 'rotate based on position of letter d') == 'ecabd'

    from aocd.models import Puzzle
    puz = Puzzle(2016, 21)

    puz.answer_a = scrambler('abcdefgh', puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = descrambler('fbgdceah', puz.input_data)
    print('Part 2:', puz.answer_b)
