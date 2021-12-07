from collections import namedtuple


RuleItem = namedtuple('RuleItem', 'num color')


def simplify(bag):
    return bag.replace('bags', '').replace('bag', '').strip()


def get_count(bag):
    if bag == 'no other':
        num, color = 0, 'other'
    else:
        num, color = bag.split(' ', maxsplit=1)
    return RuleItem(int(num), color)


def parse(rules):
    d = {}
    for rule in rules:
        source, fill = rule[:-1].split('contain')
        source = simplify(source)
        if ',' not in fill:
            fill = [get_count(simplify(fill))]
        else:
            fill = [get_count(simplify(b)) for b in fill.split(',')]
        d[source] = fill
    return d


def check_bag(bag, options):
    return any(bag in option for option in options)


# Depth first search through the graph of parent -> children
# Would have been simpler to just assemble a graph of child -> parents from the input
def search(bags, target):
    frontier = [[b] for b in bags]
    reaches = set()
    seen = set()
    while frontier:
        path = frontier.pop()
        last_bag = path[-1]

        if last_bag in reaches or target in last_bag == target:
            reaches |= set(path)

        if last_bag in seen or last_bag not in bags:
            continue

        seen |= {last_bag}
        for item in bags[last_bag]:
            frontier.append(path + [item.color])

    return reaches - {target}


def total_bags(bags, start):
    todo = list(bags[start])
    count = 0
    while todo:
        next_bag = todo.pop()
        count += next_bag.num
        if next_bag.color in bags:
            for bag in bags[next_bag.color]:
                todo.append(bag._replace(num=bag.num * next_bag.num))
    return count


if __name__ == '__main__':
    from aocd.models import Puzzle

    my_bag = 'shiny gold'

    t='''light red bags contain 1 bright white bag, 2 muted yellow bags.
    dark orange bags contain 3 bright white bags, 4 muted yellow bags.
    bright white bags contain 1 shiny gold bag.
    muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
    shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
    dark olive bags contain 3 faded blue bags, 4 dotted black bags.
    vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
    faded blue bags contain no other bags.
    dotted black bags contain no other bags.'''

    rules = parse(t.split('\n'))

    assert len(search(rules, my_bag)) == 4
    assert total_bags(rules, my_bag) == 32

    t = '''shiny gold bags contain 2 dark red bags.
    dark red bags contain 2 dark orange bags.
    dark orange bags contain 2 dark yellow bags.
    dark yellow bags contain 2 dark green bags.
    dark green bags contain 2 dark blue bags.
    dark blue bags contain 2 dark violet bags.
    dark violet bags contain no other bags.'''

    rules = parse(t.split('\n'))
    assert total_bags(rules, my_bag) == 126

    puz = Puzzle(2020, 7)
    rules = parse(puz.input_data.split('\n'))

    puz.answer_a = len(search(rules, my_bag))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = total_bags(rules, my_bag)
    print(f'Part 2: {puz.answer_b}')
