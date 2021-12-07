from collections import deque
import functools


def parse(s):
    food = []
    for line in s.split('\n'):
        i, a = line.split(' (contains ')
        ingredients = set(i.lstrip().split(' '))
        allergens = set(a[:-1].split(', '))
        food.append((ingredients, allergens))
    return food


def match_possible_allergens(food):
    possible = {}
    for items, aller in food:
        for a in aller:
            if a in possible:
                possible[a] = possible[a] & items
            else:
                possible[a] = items

    return possible


def get_safe(food):
    possible = match_possible_allergens(food)
    suspect = functools.reduce(set.union, possible.values())
    all_ingreds = {i for r in food for i in r[0]}

    return all_ingreds - suspect


def determine_allergens(food):
    firm = {}
    queue = deque((allergen, options) for allergen, options in match_possible_allergens(food).items())
    while queue:
        allergen, options = queue.pop()
        options -= set(firm.values())
        if len(options) == 1:
            firm[allergen] = tuple(options)[0]
        else:
            queue.appendleft((allergen, options))

    return firm


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
    trh fvjkl sbzzf mxmxvkd (contains dairy)
    sqjhc fvjkl (contains soy)
    sqjhc mxmxvkd sbzzf (contains fish)'''

    food = parse(t)
    safe = get_safe(food)
    assert sum(i in r for r,_ in food for i in safe) == 5

    allergens = determine_allergens(food)
    assert ','.join(allergens[aller] for aller in sorted(allergens)) == 'mxmxvkd,sqjhc,fvjkl'

    puz = Puzzle(2020, 21)
    food = parse(puz.input_data)

    safe = get_safe(food)
    puz.answer_a = sum(i in r for r,_ in food for i in safe)
    print(f'Part 1: {puz.answer_a}')

    allergens = determine_allergens(food)
    puz.answer_b = ','.join(allergens[aller] for aller in sorted(allergens))
    print(f'Part 2: {puz.answer_b}')
