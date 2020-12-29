import json


def walk(d, ignore_val=None):
    it = getattr(d, 'values', lambda: iter(d))
    total = 0
    for v in it():
        if isinstance(v, int):
            total += v
        elif isinstance(v, list):
            total += walk(v, ignore_val)
        elif isinstance(v, dict) and ignore_val not in v.values():
            total += walk(v, ignore_val)
    return total


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2015, 12)
    data = json.loads(puz.input_data)

    puz.answer_a = walk(data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = walk(data, 'red')
    print(f'Part 2: {puz.answer_b}')