def parse(s):
    grid = set()
    for line in s.split('\n'):
        fixed, vein = line.split(',')
        axis_fixed, val = fixed.split('=')
        axis_vein, rng = vein.split('=')
        start, end = map(int, rng.split('..'))
        if axis_fixed == 'x':
            grid |= set((int(val), y) for y in range(start, end + 1))
        else:
            grid |= set((x, int(val)) for x in range(start, end + 1))
    return grid


def flow(clay, source=(500, 0)):
    miny = min(i[1] for i in clay)
    maxy = max(i[1] for i in clay)

    sourcex, sourcey = source
    sources = [(sourcex, max(miny, sourcey))]
    water = {}
    while sources:
        x, y = sources.pop()
        water[(x, y)]= True

        # Flow down so long we don't hit clay
        while (down := (x, y + 1)) not in clay:
            # If we go off the bottom stop. Also stop
            # if we hit flowing water, which means we've done the flow from here already.
            if y >= maxy or water.get(down, False):
                break
            water[down] = True
            y += 1
        else: # We hit clay, flow sideways and fill
            blocked = True
            while blocked:
                downy = y + 1
                flowing = set()
                # Flow both left and right, keeping track of what we add as water
                for inc in (-1, 1):
                    nextx = x
                    while (nextx, y) not in clay:
                        water[(nextx, y)] = True
                        flowing.add((nextx, y))
                        down = (nextx, downy)
                        # The downwards cell is neither clay nor stopped water, we're free!
                        if down not in clay and water.get(down, True):
                            sources.append(down)
                            blocked = False
                            break
                        nextx += inc
                # Water hasn't escaped, so mark this row as not flowing--needed here
                # so we can flow on top of it.
                if blocked:
                    for loc in flowing:
                        water[loc] = False
                y -= 1
    return water


if __name__ == '__main__':
    from aocd.models import Puzzle

    s = '''x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504'''

    clay = parse(s)
    water = flow(clay)
    assert len(water) == 57
    assert sum(not v for v in water.values()) == 29

    puz = Puzzle(2018, 17)
    clay = parse(puz.input_data)
    water = flow(clay)

    puz.answer_a = len(water)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = sum(not v for v in water.values())
    print(f'Part 2: {puz.answer_b}')
