import itertools


def offset_fft(digits):
    out = [digits[-1]]
    for i in range(2, len(digits) + 1):
        out.append(out[-1] + digits[-i])
    return [abs(i) % 10 for i in reversed(out)]


def phases_off(digits, n, off):
    digits = digits[off:]
    for _ in range(n):
        digits = offset_fft(digits)
    return digits


def fft(digits):
    out = []
    half = len(digits) // 2
    for i in range(1, half + 1):
        repeat = itertools.cycle(itertools.chain(itertools.repeat(0, i),
                                                 itertools.repeat(1, i),
                                                 itertools.repeat(0, i),
                                                 itertools.repeat(-1, i)))
        next(repeat)
        out.append(abs(sum(i * d for i, d in zip(repeat, digits))) % 10)
    out.extend(offset_fft(digits[half:]))
    return out


def phases(digits, n):
    for _ in range(n):
        digits = fft(digits)
    return digits


def decode(digits):
    offset = int(''.join(str(i) for i in digits[:7]))
    return phases_off(digits * 10000, 100, offset)[:8]


def run(data):
    val = [int(i) for i in data]
    part_a = ''.join(str(i) for i in phases(val, 100)[:8])
    part_b = ''.join(str(i) for i in decode(val))
    return part_a, part_b


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert phases([1,2,3,4,5,6,7,8], 1) == [4,8,2,2,6,1,5,8]
    assert phases([1,2,3,4,5,6,7,8], 2) == [3,4,0,4,0,4,3,8]
    assert phases([1,2,3,4,5,6,7,8], 3) == [0,3,4,1,5,5,1,8]
    assert phases([1,2,3,4,5,6,7,8], 4) == [0,1,0,2,9,4,9,8]

    assert phases([8,0,8,7,1,2,2,4,5,8,5,9,1,4,5,4,6,6,1,9,0,8,3,2,1,8,6,4,5,5,9,5], 100)[:8] == [2,4,1,7,6,1,7,6]
    assert phases([1,9,6,1,7,8,0,4,2,0,7,2,0,2,2,0,9,1,4,4,9,1,6,0,4,4,1,8,9,9,1,7], 100)[:8] == [7,3,7,4,5,4,1,8]

    assert decode([0,3,0,3,6,7,3,2,5,7,7,2,1,2,9,4,4,0,6,3,4,9,1,5,6,5,4,7,4,6,6,4]) == [8,4,4,6,2,0,2,6]
    assert decode([0,2,9,3,5,1,0,9,6,9,9,9,4,0,8,0,7,4,0,7,5,8,5,4,4,7,0,3,4,3,2,3]) == [7,8,7,2,5,2,7,0]
    assert decode([0,3,0,8,1,7,7,0,8,8,4,9,2,1,9,5,9,7,3,1,1,6,5,4,4,6,8,5,0,5,1,7]) == [5,3,5,5,3,7,3,1]

    puz = Puzzle(2019, 16)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
