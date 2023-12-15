def hash_alg(s):
    cur = 0
    for c in s:
        cur = ((cur + ord(c)) * 17) % 256
    return cur


def arrange(seq):
    boxes = [{} for _ in range(256)]

    for cmd in seq:
        if cmd[-1] == '-':
            label = cmd[:-1]
            box = hash_alg(label)
            boxes[box].pop(label, 0)
        elif cmd[-2] == '=':
            label = cmd[:-2]
            focal_length = int(cmd[-1])
            box = hash_alg(label)
            boxes[box][label] = focal_length

    return boxes


def focal_power(boxes):
    power = 0
    for box, contents in enumerate(boxes, 1):
        for pos, lens in enumerate(contents.values(), 1):
            power += box * pos * lens
    return power


def parse(data):
    return data.split(',')


def run(data):
    seq = parse(data)
    return sum(hash_alg(s) for s in seq), focal_power(arrange(seq))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'
    assert hash_alg('HASH') == 52
    assert sum(hash_alg(s) for s in parse(sample)) == 1320
    assert focal_power(arrange(parse(sample))) == 145

    puz = Puzzle(2023, 15)

    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
