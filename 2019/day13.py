import numpy as np

from algs import chunk_iter
from intcode import Computer

def play_game(c):
    # Insert 2 quarters
    c.memory[0] = 2

    board = np.zeros((42, 26))
    score = 0
    ball_x = 0
    paddle_x = 0
    while c.running:
        c.run([np.sign(ball_x - paddle_x)])
        for x, y, t in chunk_iter(c.output, 3):
            if x == -1 and y == 0:
                score = t
            else:
                board[x, y] = t
                if t == 3:
                    paddle_x = x
                elif t == 4:
                    ball_x = x
        # Clear the output back out
        c.output = []

#     import matplotlib.pyplot as plt
#     plt.imshow(board.T, origin='upper')

    return score


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 13)
    c = Computer.fromstring(puz.input_data)
    c.run()

    puz.answer_a = sum(1 for *_, t in chunk_iter(c.output, 3) if t == 2)
    print(f'Part 1: {puz.answer_a}')

    c = Computer.fromstring(puz.input_data)
    puz.answer_b = play_game(c)
    print(f'Part 2: {puz.answer_b}')
