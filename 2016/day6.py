from collections import Counter

def build_stats(recording):
    history = []
    for line in recording.split('\n'):
        if not history:
            history = [Counter() for _ in line]
        for count, char in zip(history, line):
            count.update(char)

    return history


def recover(recording):
    stats = build_stats(recording)
    return ''.join(count.most_common(n=1)[0][0] for count in stats)


def recover2(recording):
    stats = build_stats(recording)
    return ''.join(count.most_common(n=26)[-1][0] for count in stats)

if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar'''

    assert recover(t) == 'easter'
    assert recover2(t) == 'advent'

    puz = Puzzle(2016, 6)

    puz.answer_a = recover(puz.input_data)
    print('Part 1:', puz.answer_a)

    puz.answer_b = recover2(puz.input_data)
    print('Part 2:', puz.answer_b)
