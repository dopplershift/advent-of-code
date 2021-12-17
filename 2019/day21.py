from intcode import Computer


def run(data):
    scripts = ["""NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK""",
    """NOT J J
    AND C J
    AND B J
    AND A J
    NOT J J
    OR H T
    OR E T
    AND D T
    AND T J
    RUN"""]
    parts = []
    for s in scripts:
        c = Computer.fromstring(data)
        c.run(s + '\n')
        #c.display_ascii()
        parts.append(c.output[-1])
    return parts


if __name__ == '__main__':
    from aocd.models import Puzzle

    puz = Puzzle(2019, 21)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
