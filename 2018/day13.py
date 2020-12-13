class Cart:
    directions = {'v': (0, 1), '^': (0, -1), '<': (-1, 0), '>': (1, 0)}
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dx, self.dy = self.directions[direction]
        self.nextturn = 0
    
    def move(self, network):
        self.x += self.dx
        self.y += self.dy
        path = network[self.y][self.x]
        if path in ('/', '\\'):
            self.turn(path)
        elif path == '+':
            self.handle_intersection()

    def handle_intersection(self):
        if self.nextturn == 0: # Left
            self.dx, self.dy = self.dy, -self.dx
        elif self.nextturn == 2: # Right
            self.dx, self.dy = -self.dy, self.dx
        # Otherwise go straight

        self.nextturn = (self.nextturn + 1) % 3

    def turn(self, path):
        if path == '/':
            self.dx, self.dy = -self.dy, -self.dx
        elif path == '\\':
            self.dx, self.dy = self.dy, self.dx

    def __lt__(self, other):
        return (self.y, self.x) < (other.y, other.x)
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __str__(self):
        return ('X: {0.x:3d} Y: {0.y:3d} dx: {0.dx:2d} dy: {0.dy:2d}'.format(self))
    
    __repr__ = __str__


def run(network, carts):
    tick = 0
    while True:
        tick += 1
        todo = sorted(carts)[::-1]
        done = set()
#         print(tick)
        while todo:
            cart = todo.pop()
#             print(cart)
            cart.move(network)
            if cart in (set(todo)|done):
#                 print(tick)
                return cart.x, cart.y
            done.add(cart)

            
def crash_all(network, carts):
    tick = 0
    done = carts
    while len(done) > 1:
        tick += 1
        todo = sorted(done)[::-1]
        done = set()
#         print(tick)
        while todo:
            cart = todo.pop()
            #print(cart)
            cart.move(network)
            if cart in (set(todo) | done):
                #print('Crashed:', cart)
                if cart in done:
                    done.remove(cart)
                if cart in todo:
                    todo.remove(cart)
            else:
                done.add(cart)
#         print(len(done))
    return list(done)[0].x, list(done)[0].y


def parse(s):
    carts = []
    network = s.split('\n')
    for y, row in enumerate(network):
        for x, path in enumerate(row):
            if path in Cart.directions:
                carts.append(Cart(x, y, path))
    return network, carts


if __name__ == '__main__':
    from aocd.models import Puzzle

    s = r'''/->-\        
|   |  /----\
| /-+--+-\  |
| | |  | v  |
\-+-/  \-+--/
  \------/'''
    network, carts = parse(s)

    crash = run(network, carts)
    assert crash == (7, 3)

    f2 = r'''/>-<\  
|   |  
| /<+-\
| | | v
\>+</ |
  |   ^
  \<->/'''
    network, carts = parse(f2)
    assert crash_all(network, carts) == (6, 4)

    puz = Puzzle(2018, 13)
    network, carts = parse(puz.input_data)

    puz.answer_a = run(network, carts)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = crash_all(network, carts)
    print(f'Part 2: {puz.answer_b}')