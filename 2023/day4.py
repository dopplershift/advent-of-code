def wins(winners, selected):
    return sum(s in winners for s in selected)


def parse(data):
    for line in data.split('\n'):
        card, nums = line.split(':')
        winners, selected = nums.split('|')
        yield set(map(int, winners.split())), list(map(int, selected.split()))


def run(data):
    score = 0
    cards = list(parse(data))
    card_count = [1] * len(cards)
    for i, c in enumerate(cards):
        num = wins(*c)
        for sub in range(i + 1, i + num + 1):
            card_count[sub] += card_count[i]
        score += ((1 << num) // 2)
    return score, sum(card_count)

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11'''

    test_a, test_b = run(sample)
    assert wins({41, 48, 83, 86, 17}, [83, 86, 6, 31, 17, 9, 48, 53]) == 4
    assert test_a == 13
    assert test_b == 30

    puz = Puzzle(2023, 4)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
