from collections import deque


def shortest_path(grid):
    for y, row in enumerate(grid):
        if (x := row.find('0')) >= 0:
            break
    else:
        raise RuntimeError('Start not found!')

    all_nums = set(''.join(grid)) - {'#', '.'}
    visited = set()
    options = deque([(0, (x, y), frozenset({'0'}))])
    while options:
        n, loc, nums = options.popleft()
        if (loc, nums) in visited:
            continue
        if nums == all_nums:
            return n

        visited.add((loc, nums))
        n += 1
        x, y = loc
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x = x + dx
            new_y = y + dy
            new_loc = (new_x, new_y)
            new_spot = grid[new_y][new_x]
            if new_spot != '#':
                options.append((n, new_loc, (nums | {new_spot}) if new_spot in all_nums else nums))

    raise RuntimeError('No path found!')


def shortest_path_return(grid):
    for y, row in enumerate(grid):
        if (x := row.find('0')) >= 0:
            break
    else:
        raise RuntimeError('Start not found!')

    all_nums = set(''.join(grid)) - {'#', '.'}
    visited = set()
    shortest_dist = {}
    shortest = 2**31
    options = deque([(0, (x, y), frozenset({'0'}))])
    while options:
        n, loc, nums = options.popleft()
        if n > shortest:
            break
        if (loc, nums) in visited:
            continue
        if loc not in shortest_dist:
            shortest_dist[loc] = n

        if nums == all_nums:
            shortest = min(shortest, n + shortest_dist[loc])
            continue

        visited.add((loc, nums))
        x, y = loc
        n += 1
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            new_x = x + dx
            new_y = y + dy
            new_loc = (new_x, new_y)
            new_spot = grid[new_y][new_x]
            if new_spot != '#':
                options.append((n, new_loc, (nums | {new_spot}) if new_spot in all_nums else nums))
    else:
        raise RuntimeError('No path found!')

    return shortest


if __name__ == '__main__':
    from aocd.models import Puzzle

    maze = '''###########
#0.1.....2#
#.#######.#
#4.......3#
###########'''

    assert shortest_path(maze.split('\n')) == 14
    assert shortest_path_return(maze.split('\n')) == 20

    puz = Puzzle(2016, 24)

    puz.answer_a = shortest_path(puz.input_data.split('\n'))
    print('Part 1:', puz.answer_a)

    puz.answer_b = shortest_path_return(puz.input_data.split('\n'))
    print('Part 2:', puz.answer_b)
