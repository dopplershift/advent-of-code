from ast import literal_eval
import copy
import itertools


class Number:
    def __init__(self, left, right=None):
        if right is None:
            left, right = left

        if isinstance(left, list):
            self.left = Number(*left)
        else:
            self.left = left

        if isinstance(right, list):
            self.right = Number(*right)
        else:
            self.right = right

    @classmethod
    def fromstring(cls, s):
        return cls(literal_eval(s))

    def __add__(self, other):
        return Number(copy.deepcopy(self), copy.deepcopy(other)).reduce()

    def __eq__(self, other):
        if not isinstance(other, Number):
            return False
        return self.left == other.left and self.right == other.right

    def __iter__(self):
        return iter((self.left, self.right))

    def __str__(self):
        return f'[{self.left},{self.right}]'

    __repr__ = __str__

    def reduce(self):
        while self.explode() or self.split():
            pass
        return self

    def explode(self, depth=0):
        if depth == 3:
            if isinstance(self.left, Number):
                left, right = self.left
                self.left = 0
                self._send_piece('right', right)
                return 'left', left
            if isinstance(self.right, Number):
                left, right = self.right
                self.right = 0
                self._send_piece('left', left)
                return 'right', right
        else:
            if isinstance(self.left, Number):
                res = self.left.explode(depth + 1)
                if res is not None:
                    if res is not True and res[0] == 'right':
                        self._send_piece(*res)
                        return True
                    else:
                        return res
            if isinstance(self.right, Number):
                res = self.right.explode(depth + 1)
                if res not in (None, True):
                    if res[0] == 'left':
                        self._send_piece(*res)
                        return True
                return res

    def _send_piece(self, direc, val):
        node = getattr(self, direc)
        if isinstance(node, int):
            setattr(self, direc, node + val)
        else:
            node._add_piece('left' if direc == 'right' else 'right', val)

    def _add_piece(self, which, val):
        node = getattr(self, which)
        if isinstance(node, int):
            setattr(self, which, node + val)
        else:
            node._add_piece(which, val)

    def split(self):
        return self._check_split('left') or self._check_split('right')

    def _check_split(self, which):
        val = getattr(self, which)
        if isinstance(val, Number):
            return val.split()
        elif val >= 10:
            setattr(self, which, Number(val // 2, val - val // 2))
            return True

    @property
    def magnitude(self):
        return (3 * getattr(self.left, 'magnitude', self.left) +
                2 * getattr(self.right, 'magnitude', self.right))


def total(data):
    nums = [Number.fromstring(l) for l in data.split('\n')]
    return sum(nums[1:], nums[0])


def max_mag(data):
    nums = [Number.fromstring(l) for l in data.split('\n')]
    return max((x + y).magnitude for x, y in itertools.permutations(nums, 2))


def run(data):
    return total(data).magnitude, max_mag(data)


if __name__ == '__main__':
    from aocd.models import Puzzle

    num = Number(1, 2) + Number([3, 4], 5)
    assert num == Number([[1,2],[[3,4],5]])
    assert num.magnitude == 143

    num = Number([[[[[9,8],1],2],3],4])
    num.explode()
    assert num == Number([[[[0,9],2],3],4])

    num = Number([7,[6,[5,[4,[3,2]]]]])
    num.explode()
    assert num == Number([7,[6,[5,[7,0]]]])

    num = Number([[6,[5,[4,[3,2]]]],1])
    num.explode()
    assert num == Number([[6,[5,[7,0]]],3])

    num = Number([[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]])
    num.explode()
    assert num == Number([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])

    num = Number([[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]])
    num.explode()
    assert num == Number([[3,[2,[8,0]]],[9,[5,[7,0]]]])

    num = Number([[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]])
    num.explode()
    assert num == Number([[[[0,7],4],[7,[[8,4],9]]],[1,1]])
    num.explode()
    assert num == Number([[[[0,7],4],[15,[0,13]]],[1,1]])
    num.split()
    assert num == Number([[[[0,7],4],[[7,8],[0,13]]],[1,1]])
    num.split()
    assert num == Number([[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]])
    num.explode()
    assert num == Number([[[[0,7],4],[[7,8],[6,0]]],[8,1]])
    assert num.magnitude == 1384

    num = Number([[[[4,3],4],4],[7,[[8,4],9]]]) + Number(1, 1)
    assert num == Number([[[[0,7],4],[[7,8],[6,0]]],[8,1]])

    sample = '''[1,1]
[2,2]
[3,3]
[4,4]'''
    t = total(sample)
    assert t == Number([[[[1,1],[2,2]],[3,3]],[4,4]])
    assert t.magnitude == 445

    sample = '''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]'''
    t = total(sample)
    assert t == Number([[[[3,0],[5,3]],[4,4]],[5,5]])
    assert t.magnitude == 791

    sample = '''[1,1]
[2,2]
[3,3]
[4,4]
[5,5]
[6,6]'''
    t = total(sample)
    assert t == Number([[[[5,0],[7,4]],[5,5]],[6,6]])
    assert t.magnitude == 1137

    assert Number([[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]) + Number([7,[[[3,7],[4,3]],[[6,3],[8,8]]]]) == Number([[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]])

    sample = '''[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]'''
    t = total(sample)
    assert t == Number([[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]])
    assert t.magnitude == 3488

    sample = '''[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]'''
    test_a, test_b = run(sample)
    assert test_a == 4140
    assert test_b == 3993

    puz = Puzzle(2021, 18)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
