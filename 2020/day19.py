def parse(s):
    r, m = s.split('\n\n')
    
    rules = {}
    for line in r.split('\n'):
        num, pat = line.split(': ')
        num = int(num)
        if '"' in pat:
            pat = pat.strip()[1:-1]
        elif '|' in pat:
            pat = [tuple(map(int, pair.split())) for pair in pat.split(' | ')]
        else:
            pat = tuple(map(int, pat.split()))
        rules[num] = pat
    return rules, m.split('\n')


def recursive_match(m, pos, rules, pat):
    # List means match *any*
    if isinstance(pat, list):
        for r in pat:
            yield from recursive_match(m, pos, rules, r)
    # Tuple means match *all*
    elif isinstance(pat, tuple):
        val = pat[0]
        for chars in recursive_match(m, pos, rules, rules[val]):
            if pat[1:]:
                yield from recursive_match(m, chars, rules, pat[1:])
            else:
                yield chars
    elif isinstance(pat, str):
        if pos < len(m) and m[pos] == pat:
            yield pos + 1


def match(m, rules):
    for l in recursive_match(m, 0, rules, rules[0]):
        if l == len(m):
            return True
    return False


if __name__ == '__main__':
    from aocd.models import Puzzle

    t = '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

    rules, messages = parse(t)
    for m, check in zip(messages, [True, False, True, False, False]):
        assert match(m, rules) == check, f'{m} should be {check}'

    t2 = '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''

    rules, messages = parse(t2)
    assert sum(match(m, rules) for m in messages) == 3

    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]
    assert sum(match(m, rules) for m in messages) == 12

    puz = Puzzle(2020, 19)
    rules, messages = parse(puz.input_data)

    puz.answer_a = sum(match(m, rules) for m in messages)
    print(f'Part 1: {puz.answer_a}')

    rules[8] = [(42,), (42, 8)]
    rules[11] = [(42, 31), (42, 11, 31)]

    puz.answer_b = sum(match(m, rules) for m in messages)
    print(f'Part 2: {puz.answer_b}')