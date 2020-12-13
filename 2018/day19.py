# TODO: Part 2 is still pretty slow here
from computer import Computer, parse


if __name__ == '__main__':
    from aocd.models import Puzzle

    f = '''#ip 0
    seti 5 0 1
    seti 6 0 2
    addi 0 1 0
    addr 1 2 3
    setr 1 0 0
    seti 8 0 4
    seti 9 0 5'''

    ip, code = parse(f)

    comp = Computer()
    comp.ipreg = ip
    comp.execute(code)
    assert comp.regs == [6, 5, 6, 0, 0, 9]

    puz = Puzzle(2018, 19)
    ip, code = parse(puz.input_data)

    comp = Computer()
    comp.ipreg = ip
    comp.execute(code)
    puz.answer_a = comp.regs[0]
    print(f'Part 1: {puz.answer_a}')

    # Determine reg3 by dividing rather than loop
    code[2] = ['divr', 5, 1, 3]
    code[9] = ['eqrr', 3, 3, 2] # Hack to skip loop

    comp = Computer([1, 0, 0, 0, 0, 0])
    comp.ipreg = ip
    comp.execute(code)
    puz.answer_b = comp.regs[0]
    print(f'Part 2: {puz.answer_b}')