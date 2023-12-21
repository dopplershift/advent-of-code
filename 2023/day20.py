from collections import deque
from functools import reduce
from itertools import count

from aoc_tools import lcm


def push_button(system, *, n=1000, find_cycles=False):
    highs = lows = 0
    stored_state = {}
    cycle_starts = {}
    cycles = {}

    pushes = count() if find_cycles else range(n)

    for i in pushes:
        queue = deque([('broadcaster', 0, 'button')])
        while queue:
            src, pulse, inp = queue.pop()

            if pulse:
                highs += 1
            else:
                lows += 1

            if src in system:
                kind, *dests = system[src]

                send = True
                if kind == '%':  # Flip-flop
                    if pulse:
                        send = False
                    else:
                        state = not stored_state.get(src, False)
                        stored_state[src] = state
                        pulse = int(state)
                elif kind == '&':  # Conjunction
                    if src not in stored_state:
                        memory = {inp: 0 for inp, dests in system.items() if src in dests}
                        stored_state[src] = memory

                    if find_cycles and 'rx' in dests:
                        if pulse and not stored_state[src][inp]:
                            if inp not in cycles:
                                if inp not in cycle_starts:
                                    cycle_starts[inp] = i
                                else:
                                    cycles[inp] = i - cycle_starts[inp]

                            if all(d in cycles for d in stored_state[src]):
                                return reduce(lcm, cycles.values())

                    stored_state[src][inp] = pulse
                    pulse = int(not all(stored_state[src].values()))

                if send:
                    for d in dests:
                        queue.appendleft((d, pulse, src))

    return highs * lows


def parse(data):
    system = {}
    for line in data.split('\n'):
        src, dests = line.split(' -> ')
        dests = dests.split(', ')
        if src[0] in '%&':
            system[src[1:]] = [src[0]] + dests
        else:
            system[src] = ['*'] + dests
    return system


def run(data):
    system = parse(data)
    return push_button(system), push_button(system, find_cycles=True)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = r'''broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a'''

    assert push_button(parse(sample)) == 32000000

    sample2 = r'''broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output'''

    assert push_button(parse(sample2), n=4) == 187
    assert push_button(parse(sample2)) == 11687500

    puz = Puzzle(2023, 20)

    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
