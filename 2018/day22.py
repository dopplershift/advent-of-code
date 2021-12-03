from functools import lru_cache
import heapq


@lru_cache(1000000)
def risk_level(x, y, depth, target_loc):
    return erosion_level(x, y, depth, target_loc) % 3


@lru_cache(1000000)
def erosion_level(x, y, depth, target_loc):
    return (geologic_index(x, y, depth, target_loc) + depth) % 20183


@lru_cache(1000000)
def geologic_index(x, y, depth, target_loc):
    if (x, y) == target_loc:
        return 0
    if x == 0:
        return y * 48271
    if y == 0:
        return x * 16807
    return erosion_level(x - 1, y, depth, target_loc) * erosion_level(x, y - 1, depth, target_loc)


def total_risk(depth, target):
    return sum(risk_level(i, j, depth, target) for i in range(target[0] + 1) for j in range(target[1] + 1))


def shortest_path(depth, target):
    # 0=Neither, 1=Torch, 2=Climbing to match region that can't have them
    options = [(0, 1, (0, 0))]
    types = {0, 1, 2}
    visited = set()
    while options:
        time, gear, loc = heapq.heappop(options)
        if (gear, loc) in visited:
            continue
        visited.add((gear, loc))

        if loc == target:
            if gear == 1:
                break
            else:
                heapq.heappush(options, (time + 7, 1, loc))
                continue

        time += 1
        x, y = loc
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if (newx := x + dx) >= 0 and (newy := y + dy) >= 0:
                region_type = risk_level(newx, newy, depth, target)
                if gear == region_type:  # Need to switch
                    for new_gear in types - {region_type, risk_level(x, y, depth, target)}:
                        heapq.heappush(options, (time + 7, new_gear, (newx, newy)))
                else:  # Free to move
                    heapq.heappush(options, (time, gear, (newx, newy)))

    return time


if __name__ == '__main__':
    import re
    from aocd.models import Puzzle

    target = (10, 10)
    depth = 510

    assert geologic_index(0, 0, depth, target) == 0
    assert erosion_level(0, 0, depth, target) == 510
    assert risk_level(0, 0, depth, target) == 0

    assert geologic_index(1, 0, depth, target) == 16807
    assert erosion_level(1, 0, depth, target) == 17317
    assert risk_level(1, 0, depth, target) == 1

    assert geologic_index(0, 1, depth, target) == 48271
    assert erosion_level(0, 1, depth, target) == 8415
    assert risk_level(0, 1, depth, target) == 0

    assert geologic_index(1, 1, depth, target) == 145722555
    assert erosion_level(1, 1, depth, target) == 1805
    assert risk_level(1, 1, depth, target) == 2

    assert risk_level(5, 5, depth, target) == 0
    assert risk_level(6, 5, depth, target) == 1
    assert risk_level(7, 5, depth, target) == 2

    assert geologic_index(10, 10, depth, target) == 0
    assert erosion_level(10, 10, depth, target) == 510
    assert risk_level(10, 10, depth, target) == 0

    assert total_risk(depth, target) == 114
    assert shortest_path(depth, target) == 45

    assert '\n'.join(''.join(['.', '=', '|'][risk_level(x, y, 510, (10, 10))] for x in range(16)) for y in range(16)) == '''.=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===.===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||'''

    puz = Puzzle(2018, 22)
    parsed = re.match(r'depth: (?P<depth>\d+)\ntarget: (?P<targetx>\d+),(?P<targety>\d+)', puz.input_data, re.MULTILINE|re.ASCII).groupdict()
    depth = int(parsed['depth'])
    target = (int(parsed['targetx']), int(parsed['targety']))

    puz.answer_a = total_risk(depth, target)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = shortest_path(depth, target)
    print(f'Part 2: {puz.answer_b}')