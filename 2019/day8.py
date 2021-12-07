import numpy as np

from algs import chunk_iter


def iter_layers(data, shape):
    rows, cols = shape
    for layer in chunk_iter(data, rows * cols):
        yield np.array([int(c) for c in layer]).reshape(*shape)

layer_shape = (6, 25)
BLACK = 0
WHITE = 1
TRANSPARENT = 2

if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 8)

    min_layer = min(iter_layers(puz.input_data, layer_shape), key=lambda i: (i == 0).sum())
    puz.answer_a = int((min_layer == 2).sum() * (min_layer == 1).sum())
    print(f'Part 1: {puz.answer_a}')

    image = np.full(layer_shape, TRANSPARENT, dtype=int)
    for layer in iter_layers(puz.input_data, layer_shape):
        mask = image == TRANSPARENT
        image[mask] = layer[mask]

    render = '\n'.join(''.join('#' if item == WHITE else ' ' for item in row) for row in image)
    print(render, sep='\n')

    # Found by looking at render above
    puz.answer_b = 'KAUZA'
    print(f'Part 2: {puz.answer_b}')
