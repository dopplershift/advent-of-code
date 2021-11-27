from itertools import count


def parse(s):
    try:
        return int(s)
    except ValueError:
        return s


def assemble(code):
    for line in code.split('\n'):
        op_name, op1, *op2 = line.strip().split(' ')
        yield [op_name, parse(op1), parse(op2[0]) if op2 else None]


def run(insts, **init_regs):
    regs = {r:init_regs.get(r, 0) for r in 'abcd'}
    ptr = -len(insts)
    while ptr:
        op, t1, t2 = insts[ptr]
        if op == 'inc':
            regs[t1] += 1
        elif op == 'dec':
            regs[t1] -= 1
        elif op == 'jnz':
            if regs.get(t1, t1):
                ptr += regs.get(t2, t2)
                continue
        elif op == 'cpy':
            if t2 in regs:
                regs[t2] = regs.get(t1, t1)
        elif op == 'out':
            yield regs.get(t1, t1)
        ptr += 1


def find_clock(clock):
    for i in count():
        computer = run(clock, a=i)
        prev_out = next(computer)
        correct = 0
        for out in computer:
            if out == 1 - prev_out:
                correct += 1
                prev_out = out
                if correct >= 10:
                    return i
            else:
                break


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2016, 25)
    insts = list(assemble(puz.input_data))

    puz.answer_a = find_clock(insts)
    print('Part 1:', puz.answer_a)