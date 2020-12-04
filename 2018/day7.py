from collections import defaultdict
import heapq


def parse(f):
    graph = defaultdict(list)
    deps = defaultdict(list)
    for line in f:
        parts = line.split()
        start = parts[1]
        end = parts[7]
        graph[start].append(end)
        graph[end] # Need to make sure graph has end nodes as well
        deps[end].append(start)
        deps[start]
    return graph, deps


def topo_sort(graph):
    order = []
    seen = set()
    for node in sorted(graph)[::-1]:
        visit(graph, node, order, seen)
    return order


def visit(graph, node, order, seen):
    if node in seen:
        return

    for n in sorted(graph[node])[::-1]:
        visit(graph, n, order, seen)

    seen.add(node)
    order.insert(0, node)


def process_queue(graph, deps, num_workers=5, extra=60):
    done = set()
    total_time = 0
    avail = [i for i in topo_sort(graph) if not deps[i]]

    workers = []
    tasks = deps.copy()
    while tasks or workers:
#         print('top:', tasks, workers)
        # Do we have work available and capacity
        while len(workers) < num_workers and avail:
            task = avail.pop(0)
            if task in tasks:
                heapq.heappush(workers, (total_time + extra + ord(task) - ord('A') + 1, task))
#                 print('Added worker:', total_time, (total_time + extra + ord(task) - ord('A') + 1, task))
                tasks.pop(task)

        # Need to advance the loop by peeking at the next done worker
        total_time = workers[0][0]

        # Clean up everyone that's done
        while workers and workers[0][0] == total_time:
            _, task = heapq.heappop(workers)
            done.add(task)
            for item in graph[task]:
                if not set(deps[item]) - done:
#                      print('Item available:', item)
                     avail = sorted(set(avail) | set(item)) 

    return total_time

if __name__ == '__main__':
    from aocd.models import Puzzle

    testdata = '''Step C must be finished before step A can begin.
    Step C must be finished before step F can begin.
    Step A must be finished before step B can begin.
    Step A must be finished before step D can begin.
    Step B must be finished before step E can begin.
    Step D must be finished before step E can begin.
    Step F must be finished before step E can begin.'''.split('\n')
    graph, deps = parse(testdata)

    assert topo_sort(graph) == list('CABDFE')
    assert process_queue(graph, deps, 2, 0) == 15

    puz = Puzzle(2018, 7)
    graph, deps = parse(puz.input_data.split('\n'))

    puz.answer_a = ''.join(topo_sort(graph))
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = process_queue(graph, deps)
    print(f'Part 2: {puz.answer_b}')