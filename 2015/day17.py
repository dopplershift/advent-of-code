def options(containers, total):
    if not total:
        yield ()
    elif not containers:
        return
    else:
        c = containers[0]
        if c < total:
            for opt in options(containers[1:], total - c):
                yield (c,) + opt
        elif c == total:
            yield (c,)
        yield from options(containers[1:], total)


def part2(containers, total):
    opts = list(options(containers, total))
    min_len = len(min(opts, key=lambda s: len(s)))
    return sum(len(o) == min_len for o in opts)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert len(list(options((10, 5, 5), 10))) == 2
    assert part2((10, 5, 5), 10) == 1

    assert len(list(options((20, 15, 10, 5, 5), 25))) == 4
    assert part2((20, 15, 10, 5, 5), 25) == 3

    puz = Puzzle(2015, 17)
    sizes = tuple(map(int, puz.input_data.splitlines()))

    puz.answer_a = len(list(options(sizes, 150)))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part2(sizes, 150)
    print(f'Part 2: {puz.answer_b}')
