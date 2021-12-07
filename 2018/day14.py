# TODO: Not the fastest solution

def get_recipes(n, s=None):
    if s is None:
        s = [3, 7]
    i = 0
    j = 1
    while len(s) < n + 10:
        next_recipe = s[i] + s[j]
        if next_recipe >= 10:
            s.extend(divmod(next_recipe, 10))
        else:
            s.append(next_recipe)
        i = (i + 1 + s[i]) % len(s)
        j = (j + 1 + s[j]) % len(s)
    return ''.join(str(v) for v in s[n:n+10])


def find_recipe(needle, s=None):
    if s is None:
        s = '37'
    i = 0
    j = 1
    while s.find(needle, -len(needle) - 2) == -1:
        si = int(s[i])
        sj = int(s[j])
        next_recipe = si + sj
        s += str(next_recipe)
        i = (i + 1 + si) % len(s)
        j = (j + 1 + sj) % len(s)
    return s.find(needle)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert get_recipes(9) == '5158916779'
    assert get_recipes(5) == '0124515891'
    assert get_recipes(18) == '9251071085'
    assert get_recipes(2018) == '5941429882'

    assert find_recipe('51589') == 9
    assert find_recipe('01245') == 5
    assert find_recipe('92510') == 18
    assert find_recipe('59414') == 2018

    puz = Puzzle(2018, 14)
    puz.answer_a = get_recipes(int(puz.input_data))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_recipe(puz.input_data)
    print(f'Part 2: {puz.answer_b}')
