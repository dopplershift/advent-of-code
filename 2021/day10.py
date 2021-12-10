import functools


match = dict(zip(')]}>', '([{<'))
rev_match = dict(zip(match.values(), match.keys()))
def check_line(s):
    stack = []
    for c in s:
        if c in match:
            if stack.pop() != match[c]:
                return False, c
        else:
            stack.append(c)
    return True, ''.join(rev_match[c] for c in reversed(stack))


syntax_points = {')': 3, ']': 57, '}': 1197, '>': 25137}
complete_points = {')': 1, ']': 2, '}': 3, '>': 4}
def score_complete(s):
    return functools.reduce(lambda t, c: 5 * t + complete_points[c], s, 0)


def check_code(s):
    syntax_score = 0
    completion_scores = []
    for line in s.split('\n'):
        valid, char = check_line(line)
        if valid:
            completion_scores.append(score_complete(char))
        else:
            syntax_score += syntax_points[char]
    return syntax_score, sorted(completion_scores)[len(completion_scores) // 2]

if __name__ == '__main__':
    from aocd.models import Puzzle

    assert score_complete('}}]])})]') == 288957
    assert score_complete(')}>]})') == 5566
    assert score_complete('}}>}>))))') == 1480781
    assert score_complete(']]}}]}]}>') == 995444
    assert score_complete('])}>') == 294

    assert check_line('{([(<{}[<>[]}>{[]{[(<()>') == (False, '}')
    assert check_line('[[<[([]))<([[{}[[()]]]') == (False, ')')
    assert check_line('[{[{({}]{}}([{[{{{}}([]') == (False, ']')
    assert check_line('[<(<(<(<{}))><([]([]()') == (False, ')')
    assert check_line('<{([([[(<>()){}]>(<<{{') == (False, '>')

    assert check_line('[({(<(())[]>[[{[]{<()<>>') == (True, '}}]])})]')
    assert check_line('[(()[<>])]({[<{<<[]>>(') == (True, ')}>]})')
    assert check_line('(((({<>}<{<{<>}{[]{[]{}') == (True, '}}>}>))))')
    assert check_line('{<[[]]>}<{[{[{[]{()[[[]') == (True, ']]}}]}]}>')
    assert check_line('<{([{{}}[<[[[<>{}]]]>[]]') == (True, '])}>')

    sample = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]'''
    assert check_code(sample) == (26397, 288957)

    puz = Puzzle(2021, 10)
    syntax, completion = check_code(puz.input_data)

    puz.answer_a = syntax
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = completion
    print(f'Part 2: {puz.answer_b}')
