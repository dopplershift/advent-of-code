def process(s):
    return list(map(int, s.split()))


def handle_tree(vals):
    num_children = next(vals)
    num_metadata = next(vals)
    total = 0
    for _ in range(num_children):
        total += handle_tree(vals)
    for _ in range(num_metadata):
        total += next(vals)
    return total
    

def handle_tree2(vals):
    num_children = next(vals)
    num_metadata = next(vals)
    children = [handle_tree2(vals) for _ in range(num_children)]
    metadata = [next(vals) for _ in range(num_metadata)]
    if not children:
        return sum(metadata)
    else:
        return sum(children[i - 1] for i in metadata if 1<=i<=len(children))
    
if __name__ == '__main__':
    from aocd.models import Puzzle

    vals = process('2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2')

    assert handle_tree(iter(vals)) == 138
    assert handle_tree2(iter(vals)) == 66

    puz = Puzzle(2018, 8)
    vals = process(puz.input_data)

    puz.answer_a = handle_tree(iter(vals))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = handle_tree2(iter(vals))
    print(f'Part 2: {puz.answer_b}')