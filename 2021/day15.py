import heapq


def run(data):
    grid = parse(data)
    return least_risk(grid), least_risk(grid, 5)


def parse(s):
    return [list(map(int, row)) for row in s.split('\n')]


def least_risk(layout, n=1):
    x_size = len(layout[0])
    y_size = len(layout)
    goal_x = n * x_size - 1
    goal_y = n * y_size - 1
    goal = (goal_x, goal_y)
    shortest = {}
    options = [(0, 0, 0)]
    while options:
        cost, x, y = heapq.heappop(options)
        if (x, y) == goal:
            return cost
        if cost < shortest.get((x, y), 2**32):
            shortest[x, y] = cost
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x = x + dx
                new_y = y + dy
                if 0 <= new_x <= goal_x and 0 <= new_y <= goal_y:
                    move_cost = layout[new_y % y_size][new_x % x_size] + new_x // x_size + new_y // y_size
                    if move_cost > 9:
                        move_cost %= 9
                    new_cost = cost + move_cost
                    heapq.heappush(options, (new_cost, new_x, new_y))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581'''

    test_a, test_b = run(sample)
    assert test_a == 40
    assert test_b == 315

    puz = Puzzle(2021, 15)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
