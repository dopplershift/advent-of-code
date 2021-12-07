def total(entries):
    return sum(int(l) for l in entries)

def duplicate_result(entries, start=0, seen=None):
    if seen is None:
        seen = set([0])
    freq = start
    for item in entries:
        freq += int(item)
        if freq in seen:
            return freq
        seen.add(freq)
    return duplicate_result(entries, freq, seen)

if __name__ == '__main__':
    from aocd.models import Puzzle

    assert total(['+1', '-2', '+3', '+1']) == 3
    assert total([+1, +1, +1]) == 3
    assert total([+1, +1, -2]) == 0
    assert total([-1, -2, -3]) == -6

    assert duplicate_result([+1, -1]) == 0
    assert duplicate_result([+3, +3, +4, -2, -4]) == 10
    assert duplicate_result([-6, +3, +8, +5, -6]) == 5
    assert duplicate_result([+7, +7, -2, -7, -4]) == 14

    puz = Puzzle(2018, 1)
    nums = [int(i) for i in puz.input_data.split('\n')]

    puz.answer_a = total(nums)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = duplicate_result(nums)
    print(f'Part 2: {puz.answer_b}')
