import heapq

import numpy as np

from geom import Point
from intcode import Computer


class Node:
    def __init__(self, cost, estimate, loc, parent):
        self.cost = cost
        self.estimate = estimate
        self.loc = loc
        self.parent = parent

    @property
    def total_cost(self):
        return self.cost + self.estimate

    def __lt__(self, other):
        return self.total_cost < other.total_cost


def astar(start, goal, board):
    fringe = [Node(0, start.manhattan_distance(goal), start, None)]
    done = set()
    while fringe:
        best = heapq.heappop(fringe)
        if best.loc == goal:
            break
        done.add(best.loc)
        for candidate in best.loc.neighbors:
            if board[tuple(candidate)] and candidate not in done:
                heapq.heappush(fringe, Node(best.cost + 1, candidate.manhattan_distance(goal), candidate, best))
    else:
        raise RuntimeError('Failed to find end!')

    return best


def fill(start, layout):
    time = -1
    filled = set()
    to_fill = {start}
    while to_fill:
        time += 1
        next_round = set()
        for item in to_fill:
            for candidate in item.neighbors:
                if layout[tuple(candidate)] and candidate not in filled:
                    next_round.add(candidate)
        filled |= to_fill
        to_fill = next_round
    return time


def find_layout(c, start):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4
    direc_order = [NORTH, EAST, SOUTH, WEST]
    direc_step = {NORTH:Point(0, 1), EAST:Point(1, 0), SOUTH:Point(0, -1), WEST:Point(-1, 0)}

    BLOCKED = 0
    OK = 1
    END = 2

    move = NORTH
    loc = start 
    direc = 0

    # Empirically determined size
    layout = np.full((43, 43), 3, dtype=np.int8)
    layout[tuple(start)] = 2
    move_count = 0
    while c.running:
        c.run([move])
        status = c.output.pop()

        step = direc_step[move]
        next_loc = loc + step
        if next_loc == start:
            break
        layout[tuple(next_loc)] = status

        if status == BLOCKED:
            # Turn left
            direc = (direc - 1) % 4
            move = direc_order[direc]
        elif status in (OK, END):
            # Turn right--essentially constantly tests wall on right
            move_count += 1
            loc = next_loc
            direc = (direc + 1) % 4
            move = direc_order[direc]
            if status == END:
                goal = next_loc

#     fig, ax = plt.subplots(figsize=(10, 10))
#     ax.imshow(layout.T, origin='lower')

    return layout, goal


if __name__ == '__main__':
    from aocd.models import Puzzle

    test = np.array([[3, 0, 0, 3, 3, 3],
                     [0, 1, 1, 0, 0, 3],
                     [0, 1, 0, 1, 1, 0],
                     [0, 1, 2, 1, 0, 3],
                     [3, 0, 0, 0, 3, 3]])
    src = Point(2, 3)
    assert fill(src, test.T) == 4

    puz = Puzzle(2019, 15)
    c = Computer.fromstring(puz.input_data)

    # arbitrary starting point really, just denotes a location in the grid
    start = Point(22, 20)
    layout, goal = find_layout(c, start)
    
    path = astar(start, goal, layout)
    puz.answer_a = path.cost
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = fill(goal, layout)
    print(f'Part 2: {puz.answer_b}')