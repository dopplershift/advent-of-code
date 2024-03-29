def run(data):
    graph = parse(data)
    return len(all_paths(graph)), len(all_paths(graph, can_repeat=True))


def parse(s):
    graph = {}
    for line in s.split('\n'):
        a, b = line.split('-')
        if b != 'start':
            graph.setdefault(a, []).append(b)
        if a != 'start':
            graph.setdefault(b, []).append(a)
    return graph


def all_paths(graph, *, can_repeat=False):
    todo = [(['start'], can_repeat)]
    reached = []
    while todo:
        path, repeat_available = todo.pop()
        for node in reversed(sorted(graph.get(path[-1], []))):
            new_path = path + [node]
            if node == 'end':
                reached.append(new_path)
            elif node != node.lower():
                todo.append((new_path, repeat_available))
            elif node not in path or repeat_available:
                todo.append((new_path, repeat_available and node not in path))
    return reached


if __name__ == '__main__':
    from aocd.models import Puzzle

    small = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end'''

    graph = parse(small)
    paths = all_paths(graph)
    assert len(paths) == 10
    assert not any('d' in path for path in paths)

    more_paths = all_paths(graph, can_repeat=True)
    assert len(more_paths) == 36

    sample = '''dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc'''

    test1_a, test1_b = run(sample)
    assert test1_a == 19
    assert test1_b == 103

    sample2 = '''fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW'''

    test2_a, test2_b = run(sample2)
    assert test2_a == 226
    assert test2_b == 3509

    puz = Puzzle(2021, 12)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
