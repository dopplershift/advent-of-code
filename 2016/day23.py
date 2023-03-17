def parse(s):
    try:
        return int(s)
    except ValueError:
        return s


def assemble(code):
    for line in code.split('\n'):
        op_name, op1, *op2 = line.strip().split(' ')
        yield [op_name, parse(op1), parse(op2[0]) if op2 else None]


togl_instrs = {'inc': 'dec', 'dec': 'inc', 'jnz': 'cpy', 'cpy': 'jnz', 'tgl': 'inc'}
def solve(insts, **init_regs):
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
        elif op == 'tgl':
            ind = ptr + regs.get(t1, t1)
            if -len(insts) <= ind < 0:
                insts[ind][0] = togl_instrs[insts[ind][0]]
        elif op == 'mul':  # Added by me
            regs[t2] *= regs.get(t1, t1)
        ptr += 1
    return regs['a']


if __name__ == '__main__':
    from aocd.models import Puzzle

    code = '''cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a'''

    insts = list(assemble(code))
    assert solve(insts) == 3

    puz = Puzzle(2016, 23)

    insts = list(assemble(puz.input_data))
    puz.answer_a = solve(insts, a=7)
    print('Part 1:', puz.answer_a)

    # Hack code to replace nested loops with multiplications
    insts = list(assemble(puz.input_data))
    insts[17][1] = -8
    insts[3:10] = [['cpy', 'b', 'a'], ['mul', 'd', 'a']]
    insts[7:11] = [['mul', 2, 'c']]

    puz.answer_b = solve(insts, a=12)
    print('Part 2:', puz.answer_b)
