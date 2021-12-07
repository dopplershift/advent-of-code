from collections import deque


def parse(s):
    player1, player2 = s.split('\n\n')
    player1 = list(map(int, player1.split('\n')[1:]))
    player2 = list(map(int, player2.split('\n')[1:]))
    return tuple(player1), tuple(player2)


def play(player1, player2):
    player1 = deque(player1)
    player2 = deque(player2)
    while player1 and player2:
        c1 = player1.popleft()
        c2 = player2.popleft()
        if c1 > c2:
            player1.append(c1)
            player1.append(c2)
        else:
            player2.append(c2)
            player2.append(c1)
    return player1 or player2


def play_recursive(player1, player2):
    player1_hand = deque(player1)
    player2_hand = deque(player2)
    cache = set()
    while player1_hand and player2_hand:
        if (tuple(player1_hand), tuple(player2_hand)) in cache:
            return tuple(player1_hand + player2_hand), tuple()
        else:
            cache.add((tuple(player1_hand), tuple(player2_hand)))

        c1 = player1_hand.popleft()
        c2 = player2_hand.popleft()
        if c1 <= len(player1_hand) and c2 <= len(player2_hand):
            p1, p2 = play_recursive(tuple(player1_hand)[:c1], tuple(player2_hand)[:c2])
            p1_wins = p1 > p2
        else:
            p1_wins = c1 > c2

        if p1_wins:
            player1_hand.append(c1)
            player1_hand.append(c2)
        else:
            player2_hand.append(c2)
            player2_hand.append(c1)

    return tuple(player1_hand), tuple(player2_hand)


def score(hand):
    return sum(i*c for i, c in enumerate(reversed(hand), 1))


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''Player 1:
    9
    2
    6
    3
    1

    Player 2:
    5
    8
    4
    7
    10'''

    t2 = '''Player 1:
    43
    19

    Player 2:
    2
    29
    14'''

    p1, p2 = parse(t)

    winner = play(p1, p2)
    assert score(winner) == 306

    winner = play_recursive(p1, p2)
    assert score(max(winner)) == 291
    assert play_recursive(*parse(t2))

    puz = Puzzle(2020, 22)
    p1, p2 = parse(puz.input_data)

    winner = play(p1, p2)
    puz.answer_a = score(winner)
    print(f'Part 1: {puz.answer_a}')

    winner = play_recursive(p1, p2)
    puz.answer_b = score(max(winner))
    print(f'Part 2: {puz.answer_b}')
