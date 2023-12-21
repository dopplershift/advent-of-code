from functools import reduce


def accepted_parts(system, parts):
    total = 0
    for p in parts:
        node = 'in'
        while node not in 'AR':
            for attr, op, val, next_node in system[node][:-1]:
                if ((op == '>' and p[attr] > val) or
                    (op == '<' and p[attr] < val)):
                    node = next_node
                    break
            else:
                node = system[node][-1]

        if node == 'A':
            total += sum(p.values())

    return total


def accepted_options(system):
    total = 0
    options = [({'x': range(1, 4001), 'm': range(1, 4001), 'a': range(1, 4001), 's': range(1, 4001)}, 'in')]
    while options:
        p, node = options.pop()
        if node == 'A':
            total += reduce(lambda v, r: v * len(r), p.values(), 1)
        elif node != 'R':
            for attr, op, val, next_node in system[node][:-1]:
                old_range = p[attr]
                passing = p.copy()
                if op == '>' and val + 1 in old_range:
                    p[attr] = range(old_range.start, val + 1)
                    passing[attr] = range(val + 1, old_range.stop)
                    options.append((passing, next_node))
                elif op == '<' and val - 1 in old_range:
                    passing[attr] = range(old_range.start, val)
                    p[attr] = range(val, old_range.stop)
                    options.append((passing, next_node))
            if any(len(r) for r in p.values()):
                options.append((p, system[node][-1]))

    return total


def parse(data):
    workflows, ratings = data.split('\n\n')

    system = {}
    for line in workflows.split('\n'):
        name, logic = line[:-1].split('{')
        steps = []
        for step in logic.split(','):
            if ':' in step:
                cond, node = step.split(':')
                steps.append((cond[0], cond[1], int(cond[2:]), node))
            else:
                steps.append(step)
        system[name] = steps

    parts = []
    for s in ratings.split('\n'):
        part = {}
        for i in s[1:-1].split(','):
            name, val = i.split('=')
            part[name] = int(val)
        parts.append(part)

    return system, parts


def run(data):
    system, parts = parse(data)
    return accepted_parts(system, parts), accepted_options(system)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = r'''px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}'''

    test_a, test_b = run(sample)
    assert test_a == 19114
    assert test_b == 167409079868000

    puz = Puzzle(2023, 19)

    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
