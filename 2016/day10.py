from collections import deque
import re

init_pattern = re.compile(r'value (\d+) goes to bot (\d+)', re.ASCII)
logic_pattern = re.compile(r'bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)', re.ASCII)
def run(s):
    storage = {}
    logic = {}
    output = {}
    for line in s.split('\n'):
        if match := init_pattern.match(line):
            val, bot = map(int, match.groups())
            storage.setdefault(bot, []).append(val)
        elif match := logic_pattern.match(line):
            who, dest_type1, dest1, dest_type2, dest2 = match.groups()
            logic[int(who)] = ((dest_type1, int(dest1)), (dest_type2, int(dest2)))

    answer = 0
    full = deque(bot for bot, vals in storage.items() if len(vals) == 2)
    while full:
        bot = full.pop()
        a, b = storage.pop(bot)
        if a > b:
            a, b = b, a

        if (a, b) == (17, 61):
            answer = bot

        for (dest_type, dest), val in zip(logic[bot], (a, b)):
            if dest_type == 'bot':
                items = storage.setdefault(dest, [])
                if items:
                    full.appendleft(dest)
                items.append(val)                    
            else:
                output[dest] = val

    return output, answer

if __name__ == '__main__':
    from aocd.models import Puzzle

    s = '''value 5 goes to bot 2
    bot 2 gives low to bot 1 and high to bot 0
    value 3 goes to bot 1
    bot 1 gives low to output 1 and high to bot 0
    bot 0 gives low to output 2 and high to output 0
    value 2 goes to bot 2'''

    assert run(s) == ({0: 5, 1: 2, 2: 3}, 0)

    puz = Puzzle(2016, 10)
    out, ind = run(puz.input_data)

    puz.answer_a = ind
    print('Part 1:', puz.answer_a)

    puz.answer_b = out[0] * out[1] * out[2]
    print('Part 2:', puz.answer_b)