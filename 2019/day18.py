from collections import deque
from functools import lru_cache
import heapq

from geom import Point


class Maze:
    def __init__(self, layout):
        self.layout = layout
        self.all_keys = set(c for line in layout for c in line if c.islower())
        self.multi = False

    def get_location(self, item):
        for row, line in enumerate(self.layout):
            if (col:=line.find(item)) != -1:
                break
        else:
            raise RuntimeError(f'{item} not found!')
        return (col, row) 

    def set_multi_board(self):
        # Update board with new start:
        if self.multi:
            return
        start = Point(*self.get_location('@'))
        self.layout[start.y - 1] = self.layout[start.y - 1][:start.x - 1] + '@#@' + self.layout[start.y - 1][start.x + 2:]
        self.layout[start.y] = self.layout[start.y][:start.x - 1] + '###' + self.layout[start.y][start.x + 2:]
        self.layout[start.y + 1] = self.layout[start.y + 1][:start.x - 1] + '@#@' + self.layout[start.y + 1][start.x + 2:]
        self.multi = True

    def find_starts(self):
        locs = []
        for row, line in enumerate(self.layout):
            if (col:=line.find('@')) != -1:
                locs.append((col, row))
            if (col:=line.find('@', col + 1)) != -1:
                locs.append((col, row))
        return [(col, row) for col, row in locs]

    def reachable_keys(self, start, keys):
        frontier = deque([(*start, 0)])
        seen = set()
        d = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        while frontier:
            x, y, dist = frontier.popleft()

            # Found a key
            if (key:=self.layout[y][x]).islower() and key not in keys:
                yield dist, (x, y), key
                continue

            for dx, dy in d:
                cx = x + dx
                cy = y + dy
                if (cx, cy) in seen:
                    continue
                else:
                    seen.add((cx, cy))

                loc_type = self.layout[cy][cx]

                # If it's a space, start, or a door we can pass
                if loc_type != '#' and (not loc_type.isupper() or loc_type.lower() in keys):
                    frontier.append((cx, cy, dist + 1))

    def find_dist(self):
        frontier = [(0, self.get_location('@'), frozenset())]
        seen = set()

        while frontier:
            dist, loc, keys = heapq.heappop(frontier)
            if keys == self.all_keys:
                break
            
            if (loc, keys) in seen:
                continue
            else:
                seen.add((loc, keys))

            for d, loc, key in self.reachable_keys(loc, keys):
                heapq.heappush(frontier, (dist + d, loc, keys | {key}))
        else:
            raise RuntimeError('Failed to find end!')

        return dist

    def find_dist_mult(self):
        starts = self.find_starts()
        frontier = [(0, tuple(starts), frozenset())]
        seen = [set() for _ in starts]

        while frontier:
            dist, rpos, keys = heapq.heappop(frontier)
            if keys == self.all_keys:
                break
            
            for i, loc in enumerate(rpos):
                if (loc, keys) in seen[i]:
                    continue
                else:
                    seen[i].add((loc, keys))
                
                for d, loc, key in self.reachable_keys(loc, keys):
                    new_rpos = rpos[:i] + (loc,) + rpos[i + 1:]
                    heapq.heappush(frontier, (dist + d, new_rpos, keys | {key}))
        else:
            raise RuntimeError('Failed to find end!')

        return dist

if __name__ == '__main__':
    from aocd.models import Puzzle

    test_layout = ['#########',
                   '#b.A.@.a#',
                   '#########']
    assert Maze(test_layout).find_dist() == 8

    test_layout = ['########################',
                   '#f.D.E.e.C.b.A.@.a.B.c.#',
                   '######################.#',
                   '#d.....................#',
                   '########################']
    assert Maze(test_layout).find_dist() == 86

    test_layout = ['########################',
                   '#...............b.C.D.f#',
                   '#.######################',
                   '#.....@.a.B.c.d.A.e.F.g#',
                   '########################']
    assert Maze(test_layout).find_dist() == 132

    test_layout = ['#################',
                   '#i.G..c...e..H.p#',
                   '########.########',
                   '#j.A..b...f..D.o#',
                   '########@########',
                   '#k.E..a...g..B.n#',
                   '########.########',
                   '#l.F..d...h..C.m#',
                   '#################']
    assert Maze(test_layout).find_dist() == 136

    test_layout = ['########################',
                   '#@..............ac.GI.b#',
                   '###d#e#f################',
                   '###A#B#C################',
                   '###g#h#i################',
                   '########################']
    assert Maze(test_layout).find_dist() == 81


    test_layout = ['#######',
                   '#a.#Cd#',
                   '##@#@##',
                   '#######',
                   '##@#@##',
                   '#cB#Ab#',
                   '#######']
    assert Maze(test_layout).find_dist_mult() == 8

    test_layout = ['###############',
                   '#d.ABC.#.....a#',
                   '######@#@######',
                   '###############',
                   '######@#@######',
                   '#b.....#.....c#',
                   '###############']
    assert Maze(test_layout).find_dist_mult() == 24

    test_layout = ['#############',
                   '#DcBa.#.GhKl#',
                   '#.###@#@#I###',
                   '#e#d#####j#k#',
                   '###C#@#@###J#',
                   '#fEbA.#.FgHi#',
                   '#############']
    assert Maze(test_layout).find_dist_mult() == 32

    puz = Puzzle(2019, 18)

    puz.answer_a = Maze(puz.input_data.split('\n')).find_dist()
    print(f'Part 1: {puz.answer_a}')

    m = Maze(puz.input_data.split('\n'))
    m.set_multi_board()
    puz.answer_b = m.find_dist_mult()
    print(f'Part 2: {puz.answer_b}')