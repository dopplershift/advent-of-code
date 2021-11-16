from collections import deque
from dataclasses import dataclass, field
import heapq
from geom import Point


@dataclass(order=True)
class Node:
    cost: int
    point: Point=field(compare=False)


def is_wall(x, y, bias):
    if x < 0 or y < 0:
        return True
    val = x*x + 3*x + 2*x*y + y + y*y + bias
    bit_count = 0
    while val:
        bit_count += (val & 0x1)
        val >>= 1
    return bit_count % 2 == 1


def shortest_path(x, y, val):
    """Shortest path using A*."""
    goal = Point(x, y)
    start = Point(1, 1)
    frontier = [Node(0, start)]
    min_dist = {start: 0}
    # came_from = {}
    while frontier:
        current = heapq.heappop(frontier).point
        if current == goal:
            break
        for pt in current.neighbors:
            if is_wall(*pt, val):
                continue
            if (dist := min_dist.get(current, 0) + 1) < min_dist.get(pt, 2**32):
                # came_from[pt] = current
                min_dist[pt] = dist
                heapq.heappush(frontier, Node(dist + pt.manhattan_distance(goal), pt))
    else:
        raise RuntimeError('Failed to get to destination!')

    # step_count = 0
    # while current in came_from:
    #     step_count += 1
    #     current = came_from[current]
    # return step_count

    return min_dist[goal]


def total_visited(x, y, val):
    """Flood fill with A*-style distance tracking."""
    start = Point(1, 1)
    frontier = deque([start])
    min_dist = {start: 0}
    while frontier:
        current = frontier.pop()
        for pt in current.neighbors:
            if is_wall(*pt, val):
                continue
            if (dist := min_dist.get(current, 0) + 1) <= min(min_dist.get(pt, 2**32), 50):
                min_dist[pt] = dist
                frontier.appendleft(pt)

    return len(min_dist)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert is_wall(5, 2, 10)
    assert not is_wall(7, 5, 10)
    assert not is_wall(0, 0, 10)
    assert is_wall(9, 6, 10)

    assert shortest_path(7, 4, 10) == 11
    assert total_visited(7, 4, 10) == 151

    puz = Puzzle(2016, 13)

    puz.answer_a = shortest_path(31, 39, int(puz.input_data))
    print('Part 1:', puz.answer_a)

    puz.answer_b = total_visited(31, 39, int(puz.input_data))
    print('Part 2:', puz.answer_b)