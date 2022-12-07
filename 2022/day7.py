class Directory:
    def __init__(self, parent):
        self.parent = parent
        self._subdirs = {}
        self._size = 0

    @classmethod
    def from_output(cls, output):
        pwd = root = cls(None)
        for line in output.split('\n'):
            match line.split(' '):
                case ['$', 'cd', '..']:
                    pwd = pwd.parent
                case ['$', 'cd', '/']:
                    pwd = root
                case ['$', 'cd', newdir]:
                    pwd = pwd[newdir]
                case ['$', 'ls']:
                    pass
                case [size, name]:
                    if size == 'dir':
                        pwd.add_subdir(name)
                    else:
                        pwd.add_file(name, int(size))
        return root

    def add_file(self, name, size):
        self._size += size

    def add_subdir(self, name):
        return self._subdirs.setdefault(name, type(self)(self))

    def __getitem__(self, d):
        return self._subdirs[d]

    @property
    def subdirs(self):
        return self._subdirs.values()

    @property
    def size(self):
        return self._size + sum(d.size for d in self.subdirs)

    def dirs(self):
        yield self
        for item in self.subdirs:
            yield from item.dirs()


def run(data):
    fs = Directory.from_output(data)
    needed = fs.size - (70_000_000 - 30_000_000)
    return (sum(s for d in fs.dirs() if (s := d.size) <= 100_000),
            min(s for d in fs.dirs() if (s := d.size) >= needed))


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k'''

    test_a, test_b = run(sample)
    assert test_a == 95437
    assert test_b == 24933642

    puz = Puzzle(2022, 7)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
