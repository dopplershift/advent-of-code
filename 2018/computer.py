def parse(s):
    lines = s.split('\n')
    ip = int(lines[0].split()[-1])
    code = [[line.split()[0]] + list(map(int, line.split()[1:])) for line in lines[1:]]
    return ip, code


class Computer:
    def __init__(self, regs=None):
        if regs is None:
            regs = [0] * 6
        self.regs = regs
        self.ip = 0
        self.ipreg = 0

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

    # Hacks to optimize
    def divr(self, a, b, c):
        self.regs[c] = self.regs[a] // self.regs[b]

    def divi(self, a, b, c):
        self.regs[c] = self.regs[a] // b
        
    def execute(self, code):
        counter = 0
        while self.ip < len(code):
            self.regs[self.ipreg] = self.ip
            self(*code[self.ip])
            #print(code[self.ip], self.regs)
            self.ip = self.regs[self.ipreg] + 1
            counter += 1
        return counter
    
    def __call__(self, opcode, a, b, c):
        getattr(self, opcode)(a, b, c)
