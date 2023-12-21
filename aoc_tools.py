import contextlib
import functools
import io
import itertools
from pathlib import Path
import re
import sys


def gcd(x, y):
    """Calculate the greatest common divisor of two numbers."""
    while y != 0:
        x, y = y, x % y
    return x


def lcm(a, b):
    """Calculate the least common multiple of two numbers."""
    return a * b // gcd(a, b)


def ext_euclid(a,b):
    """Extended Euclid's algorithm for GCD.
    Given input a, b the function returns d such that gcd(a,b) = d
    and x, y such that ax + by = d, as well as u, v such that au = bv."""
    if a < b:
        a, b = b, a
    u, v, x, y = 0, 1, 1, 0
    while b != 0:
        a, b, x, y, u, v = b, a % b, u, v, x - ( a // b ) * u, y - ( a // b ) * v
    return a, x, y, u, v


def pnpoly(poly, pt):
    """Calculate whether a point is in a polygon."""
    test_x, test_y = pt
    inside = False
    for p, n in zip(poly[:-1], poly[1:]):
        px, py = p
        nx, ny = n
        if (((py > test_y) != (ny > test_y)) and
        	(test_x < (nx - px) * (test_y - py) / (ny - py) + px)):
            inside = not inside

    return inside


# Taken from itertools stdlib docs
def grouper(iterable, n, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


font_samples = ['''
###  #  # ###  #  #  ##  ####  ##  ####  ### #
#  # #  # #  # #  # #  # #    #  # #      #  #
#  # #  # #  # #  # #    ###  #  # ###    #  #
###  #  # ###  #  # #    #    #  # #      #  #
# #  #  # # #  #  # #  # #    #  # #      #  #
#  #  ##  #  #  ##   ##  ####  ##  ####  ### ####
''']
decoded = ['RURUCEOEIL']

font_samples.append('''
#  #  ##  #  # ####  ##
# #  #  # #  #    # #  #
##   #  # #  #   #  #  #
# #  #### #  #  #   ####
# #  #  # #  # #    #  #
#  # #  #  ##  #### #  #
''')
decoded.append('KAUZA')

font_samples.append('''
###   ##  #### #    ###  #  # #### ###
#  # #  #    # #    #  # #  # #    #  #
#  # #      #  #    ###  #### ###  #  #
###  # ##  #   #    #  # #  # #    ###
# #  #  # #    #    #  # #  # #    #
#  #  ### #### #### ###  #  # #    #
''')
decoded.append('RGZLBHFP')

font_samples.append('''
#        ####   #####    ####   #####   #    #   ####   #
#       #    #  #    #  #    #  #    #  #    #  #    #  #
#       #       #    #  #       #    #   #  #   #       #
#       #       #    #  #       #    #   #  #   #       #
#       #       #####   #       #####     ##    #       #
#       #       #       #  ###  #         ##    #  ###  #
#       #       #       #    #  #        #  #   #    #  #
#       #       #       #    #  #        #  #   #    #  #
#       #    #  #       #   ##  #       #    #  #   ##  #
######   ####   #        ### #  #       #    #   ### #  ######
''')
decoded.append('LCPGPXGL')

font_samples.append('''
#####
#   #
#   #
#   #
#####

''')
decoded.append('□')

def letters(s):
    """Split individual letters from multiline displayed font."""
    lines = [line.rstrip() for line in s.split('\n') if line]
    chunk_size = 5 if len(lines) == 6 else 8
    while all(line.startswith(' ') for line in lines):
        lines = [line[1:] for line in lines]
    for letter in zip(*(grouper(line, chunk_size, '') for line in lines)):
        yield '\n'.join(''.join(seq).rstrip() for seq in letter)


@functools.lru_cache(1)
def build_map():
    """Build map of glyphs for ocr."""
    glyphs = dict(zip(itertools.chain(*(letters(s) for s in font_samples)), ''.join(decoded)))
    for s, truth in zip(font_samples, decoded):
        assert ocr(s, glyphs) == truth
    return glyphs


def ocr(s, glyph_map=None):
    """Perform character recognition from AOC's font."""
    if glyph_map is None:
        glyph_map = build_map()
    return ''.join(glyph_map.get(letter, '_') for letter in letters(s.replace('.', ' ')))


@contextlib.contextmanager
def update_sys_path(*paths):
    """Temporarily add path to sys.path."""
    sys.path.extend(paths)
    yield sys.path
    for p in paths:
        sys.path.remove(p)


def run_solution(year, day, data):
    import importlib
    sol_path = Path(__file__).parent
    with update_sys_path(str(sol_path), str(sol_path / f'{year}')):
        try:
            sol = importlib.import_module(f'{year}.day{day}')
            ret = sol.run(data)
        except AttributeError:
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                exec(open(sol_path / f'{year}' / f'day{day}.py', 'rt').read(), {'__name__': '__main__'})
            ret = tuple(res[0] for line in output.getvalue().splitlines()
                        if (res := re.findall(r'Part \d:\s?(.*)', line)))
    if day == 25:
        ret = ret + ('',)
    return ret
