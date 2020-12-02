import itertools
import re

from intcode import Computer

def parse_screen(s):
    dirs = []
    items = []
    name = 'Inventory'
    for line in s.split('\n'):
        if line.startswith('=='):
            name = line.strip('==').strip()
        elif line == 'Doors here lead:':
            cur_list = dirs
            cur_list.clear()
        elif line == 'Items here:' or line == 'Items in your inventory:':
            cur_list = items
            cur_list.clear()
        elif line.startswith('-'):
            cur_list.append(line[2:])
    return name, dirs, items


def walk(c):
    options = {}
    path = ['none']
    opposite = {'east': 'west', 'west': 'east', 'north': 'south', 'south': 'north'}
    bad_items = {'escape pod', 'molten lava', 'photons', 'giant electromagnet', 'infinite loop'}
    move = ''
    while True:
        c.run(move + '\n' if move else None)
        name, dirs, items = parse_screen(c.ascii_output)
        c.clear_output()
        if name not in options:
            options[name] = sorted(dirs)[::-1]
        for item in items:
            if item not in bad_items:
                c.run(f'take {item}\n')
                if 'Command?' not in c.ascii_output:
                    c.display_ascii()
                    return
        if not any(options.values()) or name == 'Security Checkpoint':
            break

        cur_opts = options[name]
        for i, opt in enumerate(cur_opts):
            if opt != opposite.get(path[-1], None):
                break
        move = cur_opts.pop(i)
        if move != opposite.get(path[-1], None):
            path.append(move)
        else:
            path.pop()


def action(s):
    c.run(s + '\n')
    ret = parse_screen(c.ascii_output)
    c.clear_output()
    return ret


def solve(c):
    _, _, all_items = action('inv')
    all_items = set(all_items)
    for item in all_items:
        action(f'drop {item}')

    too_much = []
    items = set()
    for i in range(1, len(all_items) + 1):
        for subset in itertools.combinations(all_items, i):
            subset = set(subset)
            for item in items - subset:
                action(f'drop {item}')
            for item in subset - items:
                action(f'take {item}')
            items = subset

            c.run('south\n')
            if 'Security Checkpoint' not in c.ascii_output:
                # c.display_ascii()
                return re.search('\d+', c.ascii_output)
            elif i == 1 and 'lighter' in c.ascii_output:
                too_much.append(*subset)
            c.clear_output()

        if i == 1:
            all_items -= set(too_much)


if __name__ == '__main__':
    from aocd.models import Puzzle
    
    puz = Puzzle(2019, 25)
    c = Computer.fromstring(puz.input_data)
    walk(c)
    code = solve(c)
    
    puz.answer_a = code
    print(f'Part 1: {puz.answer_a}')