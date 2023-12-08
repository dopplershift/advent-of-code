converter = {str(i): i for i in range(1, 10)}
converter2 = converter | {w: i for i, w in enumerate(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], 1)}

def value(s, conv):
    left = min(((p, d) for d in conv if (p := s.find(d)) != -1), default=None)
    if left is None:
        return 0
    right = max((p, d) for d in conv if (p := s.rfind(d)) != -1)
    return 10 * conv[left[1]] + conv[right[1]]

def run(data):
    lines = data.strip().split('\n')
    val = sum(value(line, converter) for line in lines)
    val2 = sum(value(line, converter2) for line in lines)
    return val, val2

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet'''

    assert value('1abc2', converter) == 12
    assert value('pqr3stu8vwx', converter) == 38
    assert value('a1b2c3d4e5f', converter) == 15
    assert value('treb7uchet', converter) == 77

    test_a, test_b = run(sample)
    assert test_a == 142
    assert test_b == 142

    sample2 = '''two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen'''

    assert value('two1nine', converter2) == 29
    assert value('eightwothree', converter2) == 83
    assert value('abcone2threexyz', converter2) == 13
    assert value('xtwone3four', converter2) == 24
    assert value('4nineeightseven2', converter2) == 42
    assert value('zoneight234', converter2) == 14
    assert value('7pqrstsixteen', converter2) == 76
    assert value('nineeighttworhtvxdtxp8twoneh', converter2) == 91

    test_a, test_b = run(sample2)
    assert test_a == 209
    assert test_b == 281

    puz = Puzzle(2023, 1)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
