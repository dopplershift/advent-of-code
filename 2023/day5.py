from dataclasses import dataclass

@dataclass
class Range:
    start: int
    size: int

    @property
    def end(self):
        return self.start + self.size


@dataclass
class Map:
    dest: int
    start: int
    size: int

    @property
    def end(self):
        return self.start + self.size

    def __contains__(self, val):
        return self.start <= val < self.end

    def map(self, rng):
        if rng.end <= self.end:
            return Range(rng.start + self.dest - self.start, rng.size), None
        else:
            return Range(rng.start + self.dest - self.start, self.end - rng.start), Range(self.end, rng.end - self.end)


def follow(maps, vals):
    for i, t in enumerate(maps):
        new_vals = []
        while vals:
            v = vals.pop()
            for m in t:
                if v.start in m:
                    mapped, rem = m.map(v)
                    new_vals.append(mapped)
                    if rem is not None:
                        vals.append(rem)
                    break
            else:
                new_vals.append(v)
        vals = new_vals
    return vals


def parse(data):
    blocks = data.split('\n\n')
    seeds = list(map(int, (blocks[0].split(':')[-1].split())))
    maps = []
    for b in blocks[1:]:
        lines = b.split('\n')
        maps.append(sorted([Map(*map(int, l.split())) for l in lines[1:]], key=lambda m: m.start))

    return seeds, maps


def run(data):
    seeds, maps = parse(data)

    seed_ranges = [Range(s, l) for s, l in zip(seeds[::2], seeds[1::2])]
    seeds = [Range(s, 1) for s in seeds]
    return min(r.start for r in follow(maps, seeds)), min(r.start for r in follow(maps, seed_ranges))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4'''

    test_a, test_b = run(sample)
    assert test_a == 35
    assert test_b == 46

    puz = Puzzle(2023, 5)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
