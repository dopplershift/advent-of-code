from ast import literal_eval


class Computer:
    def __init__(self, regs=None):
        if regs is None:
            regs = [0, 0, 0, 0]
        self.regs = regs

    def addr(self, a, b, c):
        self.regs[c] = self.regs[a] + self.regs[b]

    def addi(self, a, b, c):
        self.regs[c] = self.regs[a] + b

    def mulr(self, a, b, c):
        self.regs[c] = self.regs[a] * self.regs[b]

    def muli(self, a, b, c):
        self.regs[c] = self.regs[a] * b

    def banr(self, a, b, c):
        self.regs[c] = self.regs[a] & self.regs[b]

    def bani(self, a, b, c):
        self.regs[c] = self.regs[a] & b

    def borr(self, a, b, c):
        self.regs[c] = self.regs[a] | self.regs[b]

    def bori(self, a, b, c):
        self.regs[c] = self.regs[a] | b

    def setr(self, a, b, c):
        self.regs[c] = self.regs[a]

    def seti(self, a, b, c):
        self.regs[c] = a

    def gtir(self, a, b, c):
        self.regs[c] = int(a > self.regs[b])

    def gtri(self, a, b, c):
        self.regs[c] = int(self.regs[a] > b)

    def gtrr(self, a, b, c):
        self.regs[c] = int(self.regs[a] > self.regs[b])

    def eqir(self, a, b, c):
        self.regs[c] = int(a == self.regs[b])

    def eqri(self, a, b, c):
        self.regs[c] = int(self.regs[a] == b)

    def eqrr(self, a, b, c):
        self.regs[c] = int(self.regs[a] == self.regs[b])

    def train(self, commands, before, after):
        all_funcs = (self.addr, self.addi, self.mulr, self.muli,
                     self.banr, self.bani, self.borr, self.bori,
                     self.setr, self.seti, self.gtir, self.gtri,
                     self.gtrr, self.eqir, self.eqri, self.eqrr)
        opcode_map = dict()
        for b, c, a in zip(before, commands, after):
            opcode, *params = c
            options = opcode_map.setdefault(opcode, list(all_funcs))
            works = []
            for cmd in options:
                self.regs = b.copy()
                cmd(*params)
                if self.regs == a:
                    works.append(cmd)
            opcode_map[opcode] = works

        # Determine what options exist for each funciton rather than each code
        func_options = dict()
        for code, options in opcode_map.items():
            for o in options:
                func_options.setdefault(o, []).append(code)

        self._code_map = dict()
        done = set()
        while func_options:
            for func, options in sorted(func_options.items(), key=lambda i: len(i[1])):
                left = set(options) - done
                if len(left) == 1:
                    done |= left
                    self._code_map[list(left)[0]] = func
            for func in self._code_map.values():
                if func in func_options:
                    func_options.pop(func)
    
        self.regs = [0, 0, 0, 0]
    
    def __call__(self, opcode, a, b, c):
        self._code_map[opcode](a, b, c)

        
def count_works(command, before, after):
    c = Computer()
    works = 0
    for cmd in (c.addr, c.addi, c.mulr, c.muli, c.banr, c.bani, c.borr, c.bori,
                c.setr, c.seti, c.gtir, c.gtri, c.gtrr, c.eqir, c.eqri, c.eqrr):
        c.regs = before.copy()
        cmd(*command[1:])
        works += int(c.regs == after)
    return works


def parse(f):
    before = []
    command = []
    after = []
    data = list(f)
    for i in range(0, len(data), 4):
        before.append(literal_eval(data[i].split(':')[-1].strip()))
        command.append(list(map(int, data[i+1].split())))
        after.append(literal_eval(data[i+2].split(':')[-1].strip()))
    return before, command, after


def total(before, command, after):
    count = 0
    for b,c,a in zip(before, command, after):
        count += int(count_works(c, b, a) >= 3)
    return count


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert count_works([9, 2, 1, 2], [3, 2, 1, 1], [3, 2, 2, 1]) == 3

    puz = Puzzle(2018, 16)
    inp1, inp2 = puz.input_data.split('\n\n\n\n')

    before, command, after = parse(inp1.split('\n'))
    puz.answer_a = total(before, command, after)
    print(f'Part 1: {puz.answer_a}')

    comp = Computer()
    comp.train(command, before, after)
    for line in inp2.split('\n'):
        comp(*map(int, line.split()))
    puz.answer_b = comp.regs[0]
    print(f'Part 2: {puz.answer_b}')