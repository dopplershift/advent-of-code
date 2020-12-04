from collections import defaultdict
from datetime import datetime

import numpy as np


def parse(f):
    cur_guard = 0
    sleep = 0
    log = defaultdict(list)
    for line in sorted(line.lstrip() for line in f):
        dt, action = line.split(']')
        action = action.strip()
        dt = datetime.strptime(dt, '[%Y-%m-%d %H:%M')
        if action.startswith('Guard'):
            cur_guard = int(action.split('#', maxsplit=1)[1].split()[0])
        elif 'asleep' in action:
            sleep = dt.minute
        elif 'wakes' in action:
            log[cur_guard].append((sleep, dt.minute))
    return log


def strategy1(log):
    max_guard = 0
    max_total = 0
    max_minute = 0
    for guard, times in log.items():
        sleeping = np.zeros((60,), dtype=np.int)
        for start, end in times:
            sleeping[start:end] += 1
        total = sleeping.sum()
        if total > max_total:
            max_total = total
            max_guard = guard
            max_minute = sleeping.argmax()
    return max_guard * max_minute


def strategy2(log):
    guards = np.zeros((60,), dtype=np.int)
    total_sleep = np.zeros((60,), dtype=np.int)
    for guard, times in log.items():
        sleeping = np.zeros((60,), dtype=np.int)
        for start, end in times:
            sleeping[start:end] += 1
        more_asleep = sleeping > total_sleep
        guards[more_asleep] = guard
        total_sleep[more_asleep] = sleeping[more_asleep]
    best_time = total_sleep.argmax()
    return guards[best_time] * best_time


if __name__ == '__main__':
    from aocd.models import Puzzle

    testdata = '''[1518-11-01 00:00] Guard #10 begins shift
    [1518-11-01 00:05] falls asleep
    [1518-11-01 00:25] wakes up
    [1518-11-01 00:30] falls asleep
    [1518-11-01 00:55] wakes up
    [1518-11-01 23:58] Guard #99 begins shift
    [1518-11-02 00:40] falls asleep
    [1518-11-02 00:50] wakes up
    [1518-11-03 00:05] Guard #10 begins shift
    [1518-11-03 00:24] falls asleep
    [1518-11-03 00:29] wakes up
    [1518-11-04 00:02] Guard #99 begins shift
    [1518-11-04 00:36] falls asleep
    [1518-11-04 00:46] wakes up
    [1518-11-05 00:03] Guard #99 begins shift
    [1518-11-05 00:45] falls asleep
    [1518-11-05 00:55] wakes up'''.split('\n')
    log = parse(testdata)

    assert strategy1(log) == 240
    assert strategy2(log) == 4455

    puz = Puzzle(2018, 4)
    log = parse(puz.input_data.split('\n'))

    puz.answer_a = strategy1(log)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = strategy2(log)
    print(f'Part 2: {puz.answer_b}')