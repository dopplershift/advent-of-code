from intcode import Computer

if __name__ == '__main__':
    from aocd.models import Puzzle
    
    puz = Puzzle(2019, 21)

    # Hand-solved script for part 1
    script = """NOT A J
    NOT B T
    OR T J
    NOT C T
    OR T J
    AND D J
    WALK"""

    c = Computer.fromstring(puz.input_data)
    c.run(script + '\n')
    #c.display_ascii()
    puz.answer_a = c.output[-1]
    print(f'Part 1: {puz.answer_a}')

    # Hand-solved script for part 2
    script = """NOT J J
    AND C J
    AND B J
    AND A J
    NOT J J
    OR H T
    OR E T
    AND D T
    AND T J
    RUN"""

    c = Computer.fromstring(puz.input_data)
    c.run(script + '\n')
    #c.display_ascii()
    puz.answer_b = c.output[-1]
    print(f'Part 2: {puz.answer_b}')
