import numpy as np

from aoc_tools import grouper, ocr


layer_shape = (6, 25)
BLACK = 0
WHITE = 1
TRANSPARENT = 2


def run(data):
    min_layer = min(iter_layers(data, layer_shape), key=lambda i: (i == 0).sum())
    part_a = int((min_layer == 2).sum() * (min_layer == 1).sum())

    image = np.full(layer_shape, TRANSPARENT, dtype=int)
    for layer in iter_layers(data, layer_shape):
        mask = image == TRANSPARENT
        image[mask] = layer[mask]

    render = '\n'.join(''.join('#' if item == WHITE else ' ' for item in row) for row in image)
    return part_a, ocr(render)


def iter_layers(data, shape):
    rows, cols = shape
    for layer in grouper(data, rows * cols):
        yield np.array([int(c) for c in layer]).reshape(*shape)


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 8)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
