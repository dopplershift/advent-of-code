def parse(s):
    for line in s:
        op, val = line.split()
        yield op, int(val)


class Computer:
    def __init__(self, code):
        self.code = code
        self.reset()

    def reset(self):
        self.reg = 0
        self.ip = 0

    def run(self):
        seen = set()
        while self.ip < len(self.code):
            op, val = self.code[self.ip]
            if self.ip in seen:
                return False
            seen.add(self.ip)
            if op == 'nop':
                pass
            elif op == 'acc':
                self.reg += val
            elif op == 'jmp':
                self.ip += val
                continue
            self.ip += 1
        return True


def find_term(prog):
    for ip in range(len(prog)):
        code = prog.copy()
        op, _ = code[ip]
        if op == 'acc':
            continue
        elif op == 'nop':
            code[ip] = ('jmp', code[ip][1])
        elif op == 'jmp':
            code[ip] = ('nop', code[ip][1])
        c = Computer(code)
        if c.run():
            break
    return c.reg


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''nop +0
    acc +1
    jmp +4
    acc +3
    jmp -3
    acc -99
    acc +1
    jmp -4
    acc +6'''

    prog = list(parse(t.split('\n')))
    c = Computer(prog)
    c.run()
    assert c.reg == 5
    assert find_term(prog) == 8

    puz = Puzzle(2020, 8)

    prog = list(parse(puz.input_data.split('\n')))
    c = Computer(prog)
    c.run()

    puz.answer_a = c.reg
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_term(prog)
    print(f'Part 2: {puz.answer_b}')