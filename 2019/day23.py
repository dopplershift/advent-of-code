import itertools

from intcode import Computer


class NAT:
    def __init__(self, network):
        self.network = network
        self.input_data = None
        self.need_first = True
        self.output = []
    
    def run(self, _):
        if not any(c.input_data for c in self.network.values() if c is not self):
            self.output = [0, *self.input_data]

            if self.need_first:
                self.part1 = self.output[-1]
                self.need_first = False
            elif self.input_data[-1] == self.last[-1]:
                self.part2 = self.input_data[-1]
                return True
            self.last = self.input_data
    
    def send_input(self, v):
        self.input_data = v


def run_network(source):
    network = {}
    network[255] = NAT(network)
    for i in range(50):
        c = Computer.fromstring(source)
        network[i] = c
        c.send_input([i])

    comps = itertools.cycle(network.values())
    while comp:=next(comps):
        if comp.run([-1]):
            break
        while comp.output:
            y = comp.output.pop()
            x = comp.output.pop()
            addr = comp.output.pop()
            network[addr].send_input((x, y))

    return network[255]


if __name__ == '__main__':
    from aocd.models import Puzzle
    
    puz = Puzzle(2019, 23)
    nat = run_network(puz.input_data.strip())
    
    puz.answer_a = nat.part1
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = nat.part2
    print(f'Part 2: {puz.answer_b}')