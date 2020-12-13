from computer import Computer, parse

if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2018, 21)
    ip, code = parse(puz.input_data)

    comp = Computer()
    comp.ipreg = ip
    comp.regs[0] = 1797184
    puz.answer_a = comp.execute(code)
    print(f'Part 1: {puz.answer_a}')

    # Optimize their code with our div instruction
    code[17] = ['divi', 4, 256, 4]
    code[18] = code[27]

    comp = Computer()
    comp.ipreg = ip
    comp.regs[0] = 11011493
    puz.answer_b = comp.execute(code)
    print(f'Part 2: {puz.answer_b}')