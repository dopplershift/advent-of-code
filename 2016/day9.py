class Tree:
    def __init__(self, s, recurse=False):
        self._parts = []
        self._recurse = recurse
        self._parse(s)

    def _add_node(self, s, repeats):
        node = Tree(s, recurse=True) if self._recurse else s
        self._parts.append((node, repeats))

    def _add_string(self, s):
        if s:
            self._parts.append((s, 1))
        
    def _parse(self, s):
        ind = 0
        while ind < len(s):
            loc = s.find('(', ind)
            if loc == -1:
                self._add_string(s[ind:])
                break
            else:
                self._add_string(s[ind:loc])
                end = s.find(')', loc + 1)
                l, rep = map(int, s[loc + 1:end].split('x'))
                ind = end + 1 + l
                self._add_node(s[end + 1:ind], rep)
    
    def __len__(self):
        return sum(rep * len(p) for p, rep in self._parts)


# Simpler version that came to me after--the big change is just direct
# recursion to calculate only length. No data structure to represent
# the text. Also replaced manual parsing with a regular expression.
# The regex has no noticable speed impact, but does seem to make the
# code simpler.
import re

marker = re.compile(r'\((\d+)x(\d+)\)', re.ASCII)
def calc_len(s, recurse=False):
    total = 0
    ind = 0
    while ind < len(s):
        if match := marker.search(s, pos=ind):
            total += match.start() - ind
            l, rep = map(int, match.groups())
            ind = match.end() + l
            total += rep * (calc_len(s[match.end():ind], True) if recurse else l)
        else:
            total += len(s) - ind
            break

    return total

if __name__ == '__main__':
    from aocd.models import Puzzle

    for func in [lambda s, recurse=False: len(Tree(s, recurse)), calc_len]:
        assert func('ADVENT') == len('ADVENT')
        assert func('A(1x5)BC') == len('ABBBBBC')
        assert func('(3x3)XYZ') == len('XYZXYZXYZ')
        assert func('A(2x2)BCD(2x2)EFG') == len('ABCBCDEFEFG')
        assert func('(6x1)(1x3)A') == len('(1x3)A')
        assert func('X(8x2)(3x3)ABCY') == len('X(3x3)ABC(3x3)ABCY')

        assert func('(3x3)XYZ', recurse=True) == len('XYZXYZXYZ')
        assert func('X(8x2)(3x3)ABCY', recurse=True) == 20
        assert func('(27x12)(20x12)(13x14)(7x10)(1x12)A', recurse=True) == 241920
        assert func('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN', recurse=True) == 445

    puz = Puzzle(2016, 9)

    contents = puz.input_data.replace('\n', '')
    
    puz.answer_a = calc_len(contents)
    print('Part 1:', puz.answer_a)

    puz.answer_b = calc_len(contents, recurse=True)
    print('Part 2:', puz.answer_b)