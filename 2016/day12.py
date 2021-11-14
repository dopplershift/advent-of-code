def parse(s):
    try:
        return int(s)
    except ValueError:
        return s

def assemble(code):
    for line in code.split('\n'):
        op_name, op1, *op2 = line.strip().split(' ')
        yield (op_name, parse(op1), parse(op2[0]) if op2 else None)

def run(code, **init_regs):
    insts = list(assemble(code))
    regs = {r:init_regs.get(r, 0) for r in 'abcd'}
    ptr = 0
    while ptr < len(insts):
        op, t1, t2 = insts[ptr]
        if op == 'inc':
            regs[t1] += 1
        elif op == 'dec':
            regs[t1] -= 1
        elif op == 'jnz':
            if regs.get(t1, t1):
                ptr += t2
                continue
        elif op == 'cpy':
            regs[t2] = regs.get(t1, t1)
        ptr += 1
    return regs['a']


if __name__ == '__main__':
    from aocd.models import Puzzle

    code = '''cpy 41 a
    cpy a b
    jnz 1 1
    inc a
    inc a
    dec a
    jnz a 2
    dec a'''
    assert run(code) == 42

    puz = Puzzle(2016, 12)

    puz.answer_a = run(puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = run(puz.input_data, c=1)
    print('Part 2:', puz.answer_b)