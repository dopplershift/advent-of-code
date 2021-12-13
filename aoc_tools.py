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


def chunk_iter(seq, size):
    '''Iterate over sequence in fixed size chunks.'''
    for ind in range(0, len(seq), size):
        yield seq[ind:ind + size]


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
#    #### ###   ##  ###  #     ##  ####
#    #    #  # #  # #  # #    #  #    #
#    ###  #  # #    #  # #    #      #
#    #    ###  #    ###  #    # ##  #
#    #    #    #  # #    #    #  # #
#### #### #     ##  #    ####  ### ####
''')
decoded.append('LEPCPLGZ')

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


def letters(s):
    """Split individual letters from multiline displayed font."""
    lines = [line.rstrip() for line in s.split('\n') if line]
    width, spacing = (4, 1) if len(lines) == 6 else (6, 2)
    while all(line.startswith(' ') for line in lines):
        lines = [line[1:] for line in lines]
    for letter in zip(*(chunk_iter(line, width + spacing) for line in lines)):
        yield '\n'.join(seq.rstrip() for seq in letter)


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
