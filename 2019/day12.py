import copy
import itertools

import numpy as np

from algs import gcd

class Moon:
    def __init__(self, x, y, z, vel=None):
        self.pos = np.array([x, y, z])
        if vel is None:
            vel = (0, 0, 0)
        self.vel = np.array(vel)

    @classmethod
    def fromstring(cls, s):
        parts = s.strip().split(',')
        return cls(int(parts[0].split('=')[-1]),
                   int(parts[1].split('=')[-1]),
                   int(parts[2].split('=')[-1][:-1]))

    def __str__(self):
        return (f'pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, ' +
                f'vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>')

    def __repr__(self):
        return f'{type(self).__name__}({self.pos[0]}, {self.pos[1]}, {self.pos[2]})'

    def gravity(self, other):
        diff = other.pos - self.pos
        self.vel += np.sign(diff)
        other.vel -= np.sign(diff)

    def move(self):
        self.pos += self.vel

    def __eq__(self, other):
        return (self.pos == other.pos).all() and (self.vel == other.vel).all()

    @property
    def total_energy(self):
        return self.potential_energy * self.kinetic_energy

    @property
    def potential_energy(self):
        return np.abs(self.pos).sum()

    @property
    def kinetic_energy(self):
        return np.abs(self.vel).sum()

    def __copy__(self):
        return type(self)(*self.pos, np.array(self.vel))


def parse(fobj):
    for line in fobj:
        yield Moon.fromstring(line)


def run(moons, n):
    for i in range(n):
        _step(moons)


def run_to_repeat(moons):
    orig_moons = copy.deepcopy(moons)
    steps = [0] * 3
    cycled = [False] * 3
    while not all(cycled):
        _step(moons)
        for ind, status in enumerate(cycled):
            if not status:
                steps[ind] += 1
                if all(moon.pos[ind] == orig.pos[ind] and moon.vel[ind] == 0 for orig, moon in zip(orig_moons, moons)):
                    cycled[ind] = True
    return steps


def find_cycle_count(moons):
    xc, yc, zc = run_to_repeat(moons)
    tmp = (xc * yc) // gcd(xc, yc)
    return (tmp * zc) // gcd(tmp, zc)


def _step(moons):
    for m1, m2 in itertools.combinations(moons, 2):
        m1.gravity(m2)

    for m in moons:
        m.move()


if __name__ == '__main__':
    from aocd.models import Puzzle

    moons = list(parse('''<x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>'''.split('\n')))
    run(moons, 10)

    assert moons[0] == Moon(2, 1, -3, (-3, -2, 1))
    assert moons[1] == Moon(1, -8, 0, (-1, 1, 3))
    assert moons[2] == Moon(3, -6, 1, (3, 2, -3))
    assert moons[3] == Moon(2, 0, 4, (1, -1, -1))
    assert sum(m.total_energy for m in moons) == 179

    moons = list(parse('''<x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>'''.split('\n')))
    run(moons, 100)

    assert moons[0] == Moon(8, -12, -9, (-7, 3, 0))
    assert moons[1] == Moon(13, 16, -3, (3, -11, -5))
    assert moons[2] == Moon(-29, -11, -1, (-3, 7, 4))
    assert moons[3] == Moon(16, -13, 23, (7, 1, 1))
    assert sum(m.total_energy for m in moons) == 1940

    # Part 2 tests
    moons = list(parse('''<x=-1, y=0, z=2>
    <x=2, y=-10, z=-7>
    <x=4, y=-8, z=8>
    <x=3, y=5, z=-1>'''.split('\n')))
    assert find_cycle_count(moons) == 2772

    moons = list(parse('''<x=-8, y=-10, z=0>
    <x=5, y=5, z=10>
    <x=2, y=-7, z=3>
    <x=9, y=-8, z=-3>'''.split('\n')))
    assert find_cycle_count(moons) == 4686774924


    puz = Puzzle(2019, 12)
    moons = list(parse(puz.input_data.split('\n')))
    run(moons, 1000)
    puz.answer_a = int(sum(m.total_energy for m in moons))
    print(f'Part 1: {puz.answer_a}')

    moons = list(parse(puz.input_data.split('\n')))
    puz.answer_b = find_cycle_count(moons)
    print(f'Part 2: {puz.answer_b}')
