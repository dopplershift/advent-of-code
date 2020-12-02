from collections import defaultdict
import itertools

def readcode(fname):
    with open(fname, 'rt') as infile:
            return [int(c) for c in infile.readline().split(',')]

class Computer:
    def __init__(self, memory, *, save_output=True, use_text_input=False, id='Comp'):
        self._opcode_map = {1: self.add, 2: self.mul, 3: self.inp, 4: self.out,
                            5: self.jnz, 6: self.jz, 7: self.lt, 8: self.eq,
                            9: self.arp, 99:self.halt}
        self.save_output = save_output
        self.use_text_input = use_text_input
        self.id = id
        self.reset(memory)

    @classmethod
    def fromfile(cls, fname):
        with open(fname, 'rt') as infile:
            return cls.fromstring(infile.readline())

    @classmethod
    def fromstring(cls, s):
        return cls([int(c) for c in s.split(',')])
    
    def reset(self, memory):
        self.memory = defaultdict(lambda: 0, zip(range(len(memory)), memory))
        self.input_data = []
        self.running = True
        self.i_ptr = 0
        self.op_flags = 0
        self.rel_ptr = 0
        self.clear_output()
        
    def __str__(self):
        return f'{self.id}: {self.i_ptr} {self.op_flags} {self.memory[self.i_ptr:self.i_ptr + 8]}'

    def run(self, input_data=None):
        self.send_input(input_data)
        for opcode in self.codes():
            terminate = self._opcode_map[opcode]()
            if terminate:
                break

    def codes(self):
        while self.running:
            code = self.memory[self.i_ptr]
            self.op_flags = code // 100
            yield code % 100

    def flags(self, index):
        return (self.op_flags % 10**index) // 10**(index - 1)

    def to_addr(self, index):
        addr = self.i_ptr + index
        f = self.flags(index)
        if f == 0: # Position Mode
            return self.memory[addr]
        elif f == 1: # Immediate Mode
            return addr
        elif f == 2: # Relative Mode
            return self.rel_ptr + self.memory[addr]
        else:
            print(f'Unknown position mode {f}')
        
    def __getitem__(self, index):
        return self.memory[self.to_addr(index)]

    def __setitem__(self, index, val):
        self.memory[self.to_addr(index)] = val

    def send_input(self, input_data):
        if isinstance(input_data, str):
            input_data = [ord(c) for c in input_data]
        if input_data:
            self.input_data.extend(input_data)

    def read_input(self):
        if self.input_data:
            return self.input_data.pop(0)
        elif self.use_text_input:
            return int(input('Enter value:'))

    def write_output(self, val):
        if self.save_output:
            self.output.append(val)
        else:
            print(val)

    @property
    def ascii_output(self):
        return ''.join(chr(i) for i in itertools.takewhile(lambda c: c < 256, self.output))
    
    def clear_output(self):
        self.output = []
        
    def display_ascii(self):
        out = self.ascii_output
        print(out)
        self.output = self.output[len(out):]

    def connect_sink(self, sink):
        sink.input_data = self.output

    def halt(self):
        self.running = False
        return True

    def add(self):
        self[3] = self[1] + self[2]
        self.i_ptr += 4
    
    def mul(self):
        self[3] = self[1] * self[2]
        self.i_ptr += 4
    
    def inp(self):
        # If we get back None, there's no input available, so
        # signal termination
        if (ret := self.read_input()) is None:
            return True
        else:
            self[1] = ret
            self.i_ptr += 2

    def out(self):
        self.write_output(self[1])
        self.i_ptr += 2

    def jnz(self):
        self.i_ptr = self[2] if self[1] else self.i_ptr + 3

    def jz(self):
        self.i_ptr = self.i_ptr + 3 if self[1] else self[2]
    
    def lt(self):
        self[3] = int(self[1] < self[2])
        self.i_ptr += 4
    
    def eq(self):
        self[3] = int(self[1] == self[2])
        self.i_ptr += 4

    def arp(self):
        self.rel_ptr += self[1]
        self.i_ptr += 2

        
if __name__ == '__main__':
    for code, inp, outp in [([109, -1, 4, 1, 99], None, -1),
                            ([109, -1, 104, 1, 99], None, 1),
                            ([109, -1, 204, 1, 99], None, 109),
                            ([109, 1, 9, 2, 204, -6, 99], None, 204),
                            ([109, 1, 109, 9, 204, -6, 99], None, 204),
                            ([109, 1, 209, -1, 204, -106, 99], None, 204),
                            ([109, 1, 3, 3, 204, 2, 99], [15], 15),
                            ([109, 1, 203, 2, 204, 2, 99], [25], 25)]:
        c = Computer(code)
        c.run(inp)
        assert c.output == [outp]