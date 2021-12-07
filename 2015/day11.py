import itertools
import re


charmap = {chr(97 + i): chr(97 + (i + 1) % 26) for i in range(26)}
def cycle_password(start):
    digits = list(reversed(start))
    while True:
        for i, c in enumerate(digits):
            digits[i] = charmap[c]
            if c != 'z':
                break
        yield ''.join(reversed(digits))


repeated = re.compile(r'(.)\1')
def invalid(s):
    return not (any(charmap[s[i - 1]] == c and charmap[c] == s[i + 1] and c not in ('a', 'z') for i, c in enumerate(s[1:-1], 1))
            and not bool(set(s) & {'i', 'o', 'l'})
            and len(repeated.findall(s)) >= 2)


def next_password(s):
    return next(itertools.dropwhile(invalid, cycle_password(s)))


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert next_password('abcdefgh') == 'abcdffaa'
    assert next_password('ghijklmn') == 'ghjaabcc'

    puz = Puzzle(2015, 11)

    puz.answer_a = next_password(puz.input_data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = next_password(puz.answer_a)
    print(f'Part 2: {puz.answer_b}')
