import string


def collapse(s):
    changed = True
    s = [ord(c) for c in s]
    while changed:
        pointer = 0
        new_s = []
        changed = False
        while pointer < len(s) - 1:
            # Are these collapsing?
            if abs(s[pointer] - s[pointer + 1]) == 32:
                # Skip past the one we just annihilated
                pointer += 1
                changed = True
            else:
                new_s.append(s[pointer])

            # Move to the next check location    
            pointer += 1

        # Add the last item if we didn't blow it away
        if pointer < len(s):
            new_s.append(s[pointer])
        s = new_s
    return len(s)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert collapse('aA') == 0
    assert collapse('abBA') == 0
    assert collapse('abAB') == 4
    assert collapse('aabAAB') == 6
    assert collapse('dabAcCaCBAcCcaDA') == 10

    puz = Puzzle(2018, 5)
    polymer = puz.input_data

    puz.answer_a = collapse(polymer)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = min(collapse(polymer.replace(c, '').replace(c.lower(), ''))
                       for c in string.ascii_uppercase)
    print(f'Part 2: {puz.answer_b}')