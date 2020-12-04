# TODO: This solution takes forever

def marbles(p, n):
    circle = [0]
    scores = [0] * p
    cur_ind = 0
    for m in range(1, n + 1):
        if m % 23:
            cur_ind = (cur_ind + 1) % len(circle) + 1
            circle.insert(cur_ind, m)
        else:
            cur_ind = (cur_ind - 7) % len(circle)
            scores[m % p - 1] += m + circle.pop(cur_ind)
#        print(circle)
#    print(scores)
    return max(scores)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert marbles(9, 25) == 32
    assert marbles(10, 1618) == 8317
    assert marbles(13, 7999) == 146373
    assert marbles(17, 1104) == 2764
    assert marbles(21, 6111) == 54718
    assert marbles(30, 5807) == 37305

    puz = Puzzle(2018, 9)
    players = int(puz.input_data.split()[0])
    points = int(puz.input_data.split()[6])

    puz.answer_a = marbles(players, points)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = marbles(players, 100 * points)
    print(f'Part 2: {puz.answer_b}')