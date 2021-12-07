import string

from algs import BreadthFirstSearch
from geom import Point


class Maze:
    PATH = '.'

    def __init__(self, src):
        self.maze = src.split('\n')

        labels = self._get_labels()
        self.start = labels.pop('AA')[0]
        self.end = labels.pop('ZZ')[0]
        self.portals = {}
        for p1, p2 in labels.values():
            self.portals[p1] = p2
            self.portals[p2] = p1

    def _get_labels(self):
        labels = {}
        for y, line in enumerate(self.maze):
            for x, c in enumerate(line):
                if c in string.ascii_uppercase:
                    if loc := self._find_adjascent(x, y, self.PATH):
                        other_char = self.maze[2 * y - loc[1]][2 * x - loc[0]]
                        if loc > (x, y):
                            label = other_char + c
                        else:
                            label = c + other_char
                        labels.setdefault(label, []).append(loc)
        return labels

    def _find_adjascent(self, x, y, match):
        if y < len(self.maze) - 1 and self.maze[y + 1][x] in match:
            return (x, y + 1)
        elif y > 0 and self.maze[y - 1][x] in match:
            return (x, y - 1)
        elif x < len(self.maze[y]) - 1 and self.maze[y][x + 1] in match:
            return (x + 1, y)
        elif x > 0 and self.maze[y][x - 1] in match:
            return (x - 1, y)

        return None

    def find_path(self):
        bfs = BreadthFirstSearch(self.start)
        for loc in bfs:
            if loc == self.end:
                break

            if loc in self.portals:
                bfs.add(self.portals[loc])

            for candidate in Point(*loc).neighbors:
                if self.maze[candidate.y][candidate.x] == self.PATH:
                    bfs.add(tuple(candidate))
        else:
            raise RuntimeError('Failed to find end!')

        return bfs.order()


class DonutMaze(Maze):
    PATH = '.'

    def __init__(self, src):
        self.maze = src.split('\n')
        labels = self._get_labels()
        self.start = labels.pop('AA')[0]
        self.end = labels.pop('ZZ')[0]

        self.inner = {}
        self.outer = {}
        for p1, p2 in labels.values():
            if p1[0] == 2 or p1[0] == len(self.maze[0]) - 3 or p1[1] == 2 or p1[1] == len(self.maze) - 3:
                self.outer[p1] = p2
                self.inner[p2] = p1
            else:
                self.inner[p1] = p2
                self.outer[p2] = p1

    def find_path(self):
        bfs = BreadthFirstSearch((self.start, 0))
        for loc, depth in bfs:
            if loc == self.end and depth == 0:
                break

            if loc in self.outer and depth > 0:
                bfs.add((self.outer[loc], depth - 1))
            elif loc in self.inner:
                bfs.add((self.inner[loc], depth + 1))

            for candidate in Point(*loc).neighbors:
                if self.maze[candidate.y][candidate.x] == self.PATH:
                    bfs.add((tuple(candidate), depth))
        else:
            raise RuntimeError('Failed to find end!')

        return bfs.order()


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 20)

    m = Maze(puz.input_data)
    p = m.find_path()
    puz.answer_a = len(p) - 1
    print(f'Part 1: {puz.answer_a}')

    dm = DonutMaze(puz.input_data)
    p = dm.find_path()
    puz.answer_b = len(p) - 1
    print(f'Part 2: {puz.answer_b}')
