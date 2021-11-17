from collections import deque
from itertools import combinations
import re


generator_pattern = re.compile(r'(\w+) generator', re.ASCII)
microchip_pattern = re.compile(r'(\w+)-compatible microchip', re.ASCII)
def parse(s):
    d = dict()
    chips = []
    for floor, line in enumerate(s.split('\n')):
        for item in re.findall(generator_pattern, line):
            d['G' + item[:2]] = floor
        for item in re.findall(microchip_pattern, line):
            d[item[:2]] = floor
            chips.append(item[:2])
    
    state = [0] * (2 * len(chips))
    for ind, chip in enumerate(chips):
        state[2 * ind] = d[chip]
        state[2 * ind + 1] = d['G' + chip]
    state.append(len(s.split('\n')))
        
    return state


def is_safe(state):
    unprotected = set(a for (a, b) in zip(state[::2], state[1::2]) if a != b)
    gens = set(state[1::2])
    return not bool(gens & unprotected)


def get_grab_options(all_items):
    elev = all_items[-1]
    items = [ind for ind, val in enumerate(all_items[:-1]) if val == elev]
    for ind, item in enumerate(items):
        yield (item,)
        is_chip = item % 2 == 0
        for item2 in items[ind + 1:]:
            if ((is_chip and (item2 % 2 == 0 or item2 == item + 1)) or
                (not is_chip and item2 % 2 == 1)):
                yield item, item2


def get_move_options(items, grabbed, cap):
    loc = items[-1]
    new_items = list(items)
    # Don't move a pair of items downwards
    if loc > 0 and len(grabbed) < 2:
        down = loc - 1
        new_items[grabbed[0]] = down
        new_items[grabbed[-1]] = down
        new_items[-1] = down
        yield new_items
    if loc < cap:
        up = loc + 1
        new_items[grabbed[0]] = up
        new_items[grabbed[-1]] = up
        new_items[-1] = up
        yield new_items


def canonicalize(state):
    return tuple(sorted(list(zip(state[::2], state[1::2]))) + [state[-1]])


def breadth_first_search(start):
    top_floor = start[-1] - 1
    start = list(start)
    start[-1] = 0
    frontier = deque([(tuple(start), 0)])
    seen = set()
    while frontier:
        items, moves = frontier.pop()
        if all(i == top_floor for i in items[:-1]):
            break
        elif canonicalize(items) in seen:
            continue
        
        seen.add(canonicalize(items))
        for taken in get_grab_options(items):
            for new_items in get_move_options(items, taken, top_floor):
                if is_safe(new_items):
                    frontier.appendleft((tuple(new_items), moves + 1))
    else:
        raise RuntimeError('Failed to achieve goal!')

    return moves

if __name__ == '__main__':
    from aocd.models import Puzzle

    s = '''The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.'''
    start = parse(s)
    assert breadth_first_search(start) == 11

    puz = Puzzle(2016, 11)
    layout = parse(puz.input_data)

    puz.answer_a = breadth_first_search(layout)
    print('Part 1:', puz.answer_a)

    new_layout = parse(puz.input_data)
    new_layout = new_layout[:-1] + [0, 0, 0, 0] + new_layout[-1:]
    puz.answer_b = breadth_first_search(new_layout)
    print('Part 2:', puz.answer_b)