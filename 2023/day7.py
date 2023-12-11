from collections import Counter

card_order_no_jokers = '23456789TJQKA'
card_order_jokers = 'J23456789TQKA'

def order_hand(s, jokers_wild=False):
    counts = Counter(s)
    num_jokers = counts.pop('J', 0) if jokers_wild else 0

    if counts:
        biggest_group = counts.most_common(1)[0][-1] + num_jokers
        num = len(counts)
    else: # 5 jokers
        num = 1
        biggest_group = num_jokers

    card_order = card_order_jokers if jokers_wild else card_order_no_jokers

    if num == 1:
        type_score = 6
    elif num == 2:
        if biggest_group == 4:
            type_score = 5
        else:
            type_score = 4
    elif num == 3:
        if biggest_group == 3:
            type_score = 3
        else:
            type_score = 2
    elif num == 4:
        type_score = 1
    else:
        type_score = 0

    return (type_score,) + tuple(card_order.index(c) for c in s)


def parse(data):
    lines = data.split('\n')
    for line in lines:
        hand, bid = line.split()
        yield hand, int(bid)

def run(data):
    # Part 1
    ordered = sorted(parse(data), key=lambda item: (order_hand(item[0]), item[1]))
    total = sum(rank * bid for rank, (_, bid) in enumerate(ordered, 1))

    # Part 2
    ordered = sorted(parse(data), key=lambda item: (order_hand(item[0], True), item[1]))
    total_wild = sum(rank * bid for rank, (_, bid) in enumerate(ordered, 1))

    return total, total_wild


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483'''

    test_a, test_b = run(sample)
    assert test_a == 6440
    assert test_b == 5905

    puz = Puzzle(2023, 7)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
