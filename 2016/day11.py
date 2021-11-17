from collections import deque
import functools
from itertools import combinations
import operator
import re

generator_pattern = re.compile(r'(\w+) generator', re.ASCII)
microchip_pattern = re.compile(r'(\w+)-compatible microchip', re.ASCII)
def parse(s):
    return tuple(frozenset('G' + item[:2] for item in re.findall(generator_pattern, line)) | 
                 frozenset(item[:2] for item in re.findall(microchip_pattern, line))
                 for line in s.split('\n'))


def is_safe(state):
    for floor in state:
        gens = {item[1:] for item in floor if item[0] == 'G'}
        if gens:
            if {item for item in floor if item[0] != 'G'} - gens:
                return False
    return True


def get_grab_options(all_items):
    all_items = list(all_items)
    for ind, item in enumerate(all_items):
        yield {item}
        is_gen = item[0] == 'G'
        for item2 in all_items[ind + 1:]:
            if ((is_gen and (item2[0] == 'G' or item[1:] == item2)) or
                (not is_gen and (item2[0] != 'G' or item == item2[1:]))):
                yield {item, item2}


def get_move_options(items, loc, grabbed, cap):
    if loc > 0:
        down = loc - 1
        yield down, items[:down] + (items[down] | grabbed,) + (items[loc] - grabbed,) + items[loc + 1:]
    if loc < cap:
        up = loc + 1
        yield up, items[:loc] + (items[loc] - grabbed,) + (items[up] | grabbed,) + items[up + 1:]
    

def breadth_first_search(start):
    all_elem = functools.reduce(operator.or_, start)
    top_floor = len(start) - 1
    frontier = deque([(start, 0, 0)])
    seen = set()
    while frontier:
        items, elev, moves = frontier.pop()
        if items[-1] == all_elem:
            break
        elif (items, elev) in seen:
            continue
        
        seen.add((items, elev))
        for taken in get_grab_options(items[elev]):
            for new_elev, new_items in get_move_options(items, elev, taken, top_floor):
                if is_safe(new_items):
                    frontier.appendleft((new_items, new_elev, moves + 1))
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

    new_layout = (layout[0] | {'G' + 'el', 'el', 'G' + 'di', 'di'},) + layout[1:]
    puz.answer_b = breadth_first_search(new_layout)
    print('Part 2:', puz.answer_b)