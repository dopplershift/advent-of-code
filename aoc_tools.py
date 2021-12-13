import contextlib
import io
from pathlib import Path
import re
import sys


def gcd(x, y):
    """Calculate the greatest common divisor of two numbers."""
    while y != 0:
        x, y = y, x % y
    return x


def chunk_iter(seq, size):
    '''Iterate over sequence in fixed size chunks.'''
    for ind in range(0, len(seq), size):
        yield seq[ind:ind + size]


@contextlib.contextmanager
def update_sys_path(path):
    """Temporarily add path to sys.path."""
    sys.path.append(path)
    yield sys.path
    sys.path.remove(path)


def run_solution(year, day, data):
    output = io.StringIO()
    sol_path = Path(__file__).parent / f'{year}'
    with contextlib.redirect_stdout(output), update_sys_path(str(sol_path)):
        exec(open(sol_path / f'day{day}.py', 'rt').read(), {'__name__': '__main__'})
    ret = tuple(res[0] for line in output.getvalue().splitlines()
                if (res := re.findall(r'Part \d:\s?(.*)', line)))
    if day == 25:
        ret = ret + ('',)
    return ret
