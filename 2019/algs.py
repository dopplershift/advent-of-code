from collections import deque


def chunk_iter(seq, size):
    ind = 0
    while ind < len(seq):
        yield seq[ind:ind + size]
        ind += size

def gcd(x, y):
    while y != 0:
        x, y = y, x % y
    return x


class BreadthFirstSearch:
    
    def __init__(self, start, extra=()):
        self._frontier = deque([])
        self._seen = set()
        self._cur_node = None
        self.add(start, extra)
    
    def __iter__(self):
        while self._frontier:
            self._cur_node = self._frontier.pop()
            yield self._cur_node[-1]

    def add(self, item, extra=()):
        if item not in self._seen:
            self._seen.add(item)
            self._frontier.appendleft((self._cur_node, item + extra))

    def order(self):
        total_path = []
        node = self._cur_node
        while node is not None:
            total_path.append(node[-1])
            node = node[0]
        return total_path[::-1]