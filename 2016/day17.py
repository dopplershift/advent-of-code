from collections import deque
from hashlib import md5

dir_to_inc = {'U': (0, -1), 'D': (0, 1), 'L': (-1, 0), 'R': (1, 0)}

def get_options(pw, path, x, y):
    for opt, c in zip('UDLR', md5(pw + path.encode('ascii')).hexdigest()):
        if c in {'b', 'c', 'd', 'e', 'f'}:
            dx, dy = dir_to_inc[opt]
            new_x = x + dx
            new_y = y + dy
            if 0 <= new_x < 4 and 0 <= new_y < 4:
                yield new_x, new_y, path + opt


def bfs(pw):
    pw = pw.encode('ascii')
    visited = set()
    frontier = deque([(0, 0, '')])
    while frontier:
        opt = frontier.pop()
        if opt in visited:
            continue
        visited.add(opt)

        x, y, path = opt    
        if x == 3 and y == 3:
            break
        
        for opt in get_options(pw, path, x, y):
            frontier.appendleft(opt)
            
    return path


def dfs(pw):
    pw = pw.encode('ascii')
    visited = set()
    frontier = [(0, 0, '')]
    longest = ''
    while frontier:
        opt = frontier.pop()
        if opt in visited:
            continue
        visited.add(opt)

        x, y, path = opt
        if x == 3 and y == 3:
            if len(path) > len(longest):
                longest = path
            continue
        
        for opt in get_options(pw, path, x, y):
            frontier.append(opt)
            
    return longest


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert list(get_options(b'hijkl', '', 0, 0)) == [(0, 1, 'D')]
    assert list(get_options(b'hijkl', 'DU', 0, 0)) == [(1, 0, 'DUR')]

    assert bfs('ihgpwlah') == 'DDRRRD'
    assert bfs('kglvqrro') == 'DDUDRLRRUDRD'
    assert bfs('ulqzkmiv') == 'DRURDRUDDLLDLUURRDULRLDUUDDDRR'

    assert len(dfs('ihgpwlah')) == 370
    assert len(dfs('kglvqrro')) == 492
    assert len(dfs('ulqzkmiv')) == 830

    puz = Puzzle(2016, 17)

    puz.answer_a = bfs(puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = len(dfs(puz.input_data))
    print('Part 2:', puz.answer_b)