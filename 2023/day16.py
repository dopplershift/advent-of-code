def walk(grid, start=(0, 0), direc=(1, 0)):
    beams = [(*start, *direc)]
    done = set()
    while beams:
        n = beams.pop()
        if n in done:
            continue

        x, y, dx, dy = n
        if (c := grid.get((x, y), ' ')) != ' ':
            done.add(n)
            if c in './\\':
                if c == '/':
                    dx, dy = -dy, -dx
                elif c == '\\':
                    dx, dy = dy, dx
                beams.append((x + dx, y + dy, dx, dy))
            elif c == '-':
                if not dx:
                    beams.append((x - 1, y, -1, 0))
                    beams.append((x + 1, y, 1, 0))
                else:
                    beams.append((x + dx, y + dy, dx, dy))
            elif c == '|':
                if not dy:
                    beams.append((x, y - 1, 0, -1))
                    beams.append((x, y + 1, 0, 1))
                else:
                    beams.append((x + dx, y + dy, dx, dy))

    return len({(x, y) for x, y, *_ in done})


def iter_all(grid):
    max_x = max(x for x, _ in grid)
    max_y = max(y for _, y in grid)

    for x in range(max_x + 1):
        yield walk(grid, start=(x, 0), direc=(0, 1))
        yield walk(grid, start=(x, max_y), direc=(0, -1))

    for y in range(max_y + 1):
        yield walk(grid, start=(0, y), direc=(1, 0))
        yield walk(grid, start=(max_x, y), direc=(-1, 0))


def parse(data):
    return {(x, y): c for y, row in enumerate(data.split('\n')) for x, c in enumerate(row)}


def run(data):
    grid = parse(data)
    return walk(grid), max(iter_all(grid))

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....'''

    test_a, test_b = run(sample)
    assert test_a == 46
    assert test_b == 51

    puz = Puzzle(2023, 16)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
