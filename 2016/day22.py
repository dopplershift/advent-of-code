from collections import deque
import itertools
import re


node_info = re.compile(r'/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)\s+(?P<size>\d+)T\s+(?P<used>\d+)T\s+(?P<avail>\d+)T\s+\d+%',
                       re.ASCII)
def parse(s):
    for line in s.split('\n'):
        if match := re.match(node_info, line):
            d = match.groupdict()
            yield ((int(d['x']), int(d['y'])), (int(d['used']), int(d['avail']), int(d['size'])))


def viable(info):
    return sum(info[a][0] <= info[b][1] for a, b in itertools.permutations(info, 2) if info[a][0])


def shortest_path(info):
    max_x = max(k[0] for k in info)
    max_y = max(k[1] for k in info)
    immovable = {loc for loc, i in info.items() if i[2] > 100}

    for loc, (u, *_) in info.items():
        if u == 0:
            zero_loc = loc
            break

    goal_loc = (0, 0)
    frontier = deque([(0, (max_x, 0), zero_loc)])
    visited = set()
    while frontier:
        n, data_pos, zero_pos = frontier.pop()

        if data_pos == goal_loc:
            return n

        key = (data_pos, zero_pos)
        if key in visited:
            continue
        visited.add(key)

        x, y = zero_pos
        n += 1
        for dx, dy in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            move_pos = (x + dx, y + dy)
            if move_pos in info and move_pos not in immovable:
                frontier.appendleft((n, zero_pos if move_pos == data_pos else data_pos, move_pos))

    raise RuntimeError('Failed to find goal!')

if __name__ == '__main__':

    from aocd.models import Puzzle
    puz = Puzzle(2016, 22)

    info = dict(parse(puz.input_data))
    assert len(info) == 875
    assert info[0, 0] == (65, 29, 94)

    # Means no combining nodes, so we're just sliding the data around using an empty node, and there's only 1 empty node
    assert len(set(b for a, b in itertools.permutations(info, 2) if info[a][0] <= info[b][1] if info[a][0])) == 1

    puz.answer_a = viable(info)
    print('Part 1:', puz.answer_a)

    puz.answer_b = shortest_path(info)
    print('Part 2:', puz.answer_b)
