from dataclasses import dataclass


@dataclass
class Knot:
    x: int = 0
    y: int = 0

    @property
    def loc(self):
        return (self.x, self.y)

    def move(self, d: str):
        match d:
            case 'R':
                self.x += 1
            case 'L':
                self.x -= 1
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1

    def follow(self, head: Knot):
        if (dx := head.x - self.x) > 1:
            self.x += 1
            self.y = head.y
        elif dx < -1:
            self.x -= 1
            self.y = head.y
        elif (dy := head.y - self.y) > 1:
            self.y += 1
            self.x = head.x
        elif dy < -1:
            self.y -= 1
            self.x = head.x


def parse(data):
    return [(l[0], int(l[2:])) for l in data.split('\n')]


def simulate(moves, length):
    rope = [Knot() for _ in range(length)]
    history = {rope[-1].loc}
    for d, n in moves:
        for _ in range(n):
            rope[0].move(d)
            for i, knot in enumerate(rope[1:]):
                knot.follow(rope[i])
            history.add(rope[-1].loc)
    return history


def run(data):
    moves = parse(data)
    return len(simulate(moves, 2)), len(simulate(moves, 10))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2'''
    test_a, test_b = run(sample)
    assert test_a == 13
    assert test_b == 1

    sample2 = '''R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20'''
    test_a, test_b = run(sample2)
    assert test_a == 88
    assert test_b == 36

    puz = Puzzle(2022, 9)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
