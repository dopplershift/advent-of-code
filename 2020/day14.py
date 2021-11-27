import itertools


def part1(s):
    and_mask = 1
    or_mask = 0
    memory = {}
    for line in s.split('\n'):
        target, val = line.split(' = ')
        val = val.lstrip()
        if target == 'mask':
            or_mask = int(val.replace('X', '0'), 2)
            and_mask = int(val.replace('X', '1'), 2)
        elif target.startswith('mem'):
            addr = int(target[3:].replace('[', '').replace(']', ''))
            memory[addr] = (int(val) & and_mask) | or_mask
    return memory


def part2(s):
    floating = []
    mask = '0'
    memory = {}
    for line in s.split('\n'):
        target, val = line.split(' = ')
        val = val.lstrip()
        if target == 'mask':
            floating = []
            mask = 0
            for i, bit in enumerate(val):
                mask <<= 1
                if bit == '1':
                    mask |= 1
                elif bit == 'X':
                    floating.append(35 - i)
        elif target.startswith('mem'):
            addr = int(target[3:].replace('[', '').replace(']', '')) | mask
            val = int(val)
            if floating:
                for comb in itertools.product([0, 1], repeat=len(floating)):
                    new_addr = addr
                    for pos, bit in zip(floating, comb):
                        if bit:
                            new_addr |= (1<<pos)
                        else:
                            new_addr &= ~(1<<pos)
                    memory[new_addr] = val
            else:
                memory[addr] = val
    return memory


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0'''
    assert sum(part1(t).values()) == 165

    t = '''mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1'''
    assert sum(part2(t).values()) == 208

    puz = Puzzle(2020, 14)

    mem = part1(puz.input_data)
    puz.answer_a = sum(mem.values())
    print(f'Part 1: {puz.answer_a}')

    mem = part2(puz.input_data)
    puz.answer_b = sum(mem.values())
    print(f'Part 2: {puz.answer_b}')