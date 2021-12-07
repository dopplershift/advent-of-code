class Screen:
    def __init__(self, rows=6, cols=50):
        self._matrix = [[0] * cols for _ in range(rows)]

    @property
    def voltage(self):
        return sum(sum(row) for row in self._matrix)

    def rect(self, a, b):
        for r in range(b):
            row = self._matrix[r]
            for c in range(a):
                row[c] = 1

    @staticmethod
    def _rotate(seq, n):
        return seq[-n:] + seq[:-n] if n else seq

    def rotate_row(self, a, b):
        self._matrix[a] = self._rotate(self._matrix[a], b)

    def rotate_col(self, a, b):
        col = self._rotate([row[a] for row in self._matrix], b)
        for row, pixel in zip(self._matrix, col):
            row[a] = pixel

    def __call__(self, cmd):
        if cmd.startswith('rect'):
            a, b = map(int, cmd.split(' ')[-1].split('x'))
            self.rect(a, b)
        elif cmd.startswith('rotate'):
            a, b = map(int, cmd.split('=')[-1].split(' by '))
            if cmd.startswith('rotate row'):
                self.rotate_row(a, b)
            elif cmd.startswith('rotate col'):
                self.rotate_col(a, b)

    def __str__(self):
        return '\n'.join(''.join('#' if pixel else '.' for pixel in row)
                         for row in self._matrix)

    def print(self):
        print(str(self).replace('.', ' '))


if __name__ == '__main__':
    from aocd.models import Puzzle

    test = Screen(3, 7)
    test('rect 3x2')
    assert str(test) == '''###....
###....
.......'''

    test('rotate column x=1 by 1')
    assert str(test) == '''#.#....
###....
.#.....'''

    test('rotate row y=0 by 4')
    assert str(test) == '''....#.#
###....
.#.....'''

    test('rotate column x=1 by 1')
    assert str(test) == '''.#..#.#
#.#....
.#.....'''

    puz = Puzzle(2016, 8)

    screen = Screen()
    for line in puz.input_data.split('\n'):
        screen(line)

    puz.answer_a = screen.voltage
    print('Part 1:', puz.answer_a)

    screen.print()

    puz.answer_b = 'RURUCEOEIL'
    print('Part 2:', puz.answer_b)
