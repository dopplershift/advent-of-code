import heapq


def shortest_path(grid, min_travel=0, max_travel=3):
    infinity = 2**32 - 1
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)
    goal = (max_x, max_y)

    # Need to seed this with potential moves from upper left to avoid handling corner cases in loop
    todo = [(grid[move], move, move, 1) for move in [(1, 0), (0, 1)]]
    dist = {}
    while todo:
        cost, loc, move, travel = heapq.heappop(todo)

        # For part 2, need to make sure we have sufficient travel to stop
        if loc == goal and travel >= min_travel:
            return cost

        key = loc + (move, travel)
        if cost < dist.get(key, infinity):
            dist[key] = cost

            x, y = loc
            dx, dy = move

            # Continue straight
            if travel < max_travel:
                next_loc = (x + dx, y + dy)
                if next_loc in grid:
                    heapq.heappush(todo, (cost + grid[next_loc], next_loc, move, travel + 1))

            # Turn right and left
            if travel >= min_travel:
                for delta in [(-dy, dx), (dy, -dx)]:
                    next_loc = (x + delta[0], y + delta[1])
                    if next_loc in grid:
                        heapq.heappush(todo, (cost + grid[next_loc], next_loc, delta, 1))

    raise RuntimeError('No path found!')


def parse(data):
    return {(x, y): int(c) for y, row in enumerate(data.split('\n')) for x, c in enumerate(row)}


def run(data):
    grid = parse(data)
    return shortest_path(grid), shortest_path(grid, 4, 10)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = r'''2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533'''

    test_a, test_b = run(sample)
    assert test_a == 102
    assert test_b == 94

    sample2 = '''111111111111
999999999991
999999999991
999999999991
999999999991'''

    assert shortest_path(parse(sample2), 4, 10) == 71

    puz = Puzzle(2023, 17)

    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
