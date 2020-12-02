def get_orbits(src):
    orbits = {}
    for line in src:
        center, sat = line.strip().split(')')
        orbits[sat] = center
    return orbits


def count_orbits(orbits, body):
    total = 0
    while (parent := orbits.get(body)) is not None:
        total += 1
        body = parent
    return total
    

def count_total_orbits(orbits):
    total = 0
    for body in orbits:
        total += count_orbits(orbits, body)
    return total


def find_path(orbits):
    # Find the path for Santa to root node
    path = ['SAN']
    while path[-1] in orbits:
        path.append(orbits[path[-1]])
    
    # Now find our path to root until we hit something in the first path
    our_path = ['YOU']
    while our_path[-1] in orbits and our_path[-1] not in path:
        our_path.append(orbits[our_path[-1]])
    
    # Find index of intersection in first path for slicing
    ind = path.index(our_path[-1])

    # Start slices at 1 to eliminate us and Santa from path
    return our_path[1:] + path[ind - 1:0:-1]


def transfers(path):
    return len(path) - 1


if __name__ == '__main__':
    from aocd.models import Puzzle

    o = get_orbits('COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L'.split('\n'))

    assert count_orbits(o, 'D') == 3
    assert count_orbits(o, 'L') == 7
    assert count_orbits(o, 'COM') == 0
    assert count_total_orbits(o) == 42

    o = get_orbits('COM)B\nB)C\nC)D\nD)E\nE)F\nB)G\nG)H\nD)I\nE)J\nJ)K\nK)L\nK)YOU\nI)SAN'.split('\n'))
    assert transfers(find_path(o)) == 4

    puz = Puzzle(2019, 6)
    orbits = get_orbits(puz.input_data.split('\n'))

    puz.answer_a = count_total_orbits(orbits)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = transfers(find_path(orbits))
    print(f'Part 2: {puz.answer_b}')