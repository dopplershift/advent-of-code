from intcode import Computer

if __name__ == '__main__':
    from aocd.models import Puzzle

    start_code = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    c = Computer(start_code)
    c.run()
    assert c.output == start_code

    c = Computer([1102,34915192,34915192,7,4,7,99,0])
    c.run()
    assert len(str(c.output[0])) == 16

    c = Computer([104,1125899906842624,99])
    c.run()
    assert c.output == [1125899906842624]

    puz = Puzzle(2019, 9)

    c = Computer.fromstring(puz.input_data)
    c.run([1])
    puz.answer_a = c.output
    print(f'Part 1: {puz.answer_a}')

    c = Computer.fromstring(puz.input_data)
    c.run([2])
    puz.answer_b = c.output
    print(f'Part 2: {puz.answer_b}')