from intcode import Computer

def run(data):
    c = Computer.fromstring(data)
    c.run([1])
    part_a = c.output[-1]

    c = Computer.fromstring(data)
    c.run([5])
    part_b = c.output[0]

    return part_a, part_b


if __name__ == '__main__':
    from aocd.models import Puzzle

    c = Computer([1002,4,3,4,33])
    c.run()
    assert c.memory[4] == 99

    c = Computer([1101,100,-1,4,0])
    c.run()
    assert c.memory[4] == 99

    c = Computer([3,0,4,0,99])
    c.run([5])
    assert c.output[0] == 5


    for indata, outdata in zip([1, 8, 9], [0, 1, 0]):
        c = Computer([3,9,8,9,10,9,4,9,99,-1,8])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([1, 8, 9], [1, 0, 0]):
        c = Computer([3,9,7,9,10,9,4,9,99,-1,8])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([1, 8, 9], [0, 1, 0]):
        c = Computer([3,3,1108,-1,8,3,4,3,99])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([1, 8, 9], [1, 0, 0]):
        c = Computer([3,3,1107,-1,8,3,4,3,99])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([0, 100], [0, 1]):
        c = Computer([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([0, 100], [0, 1]):
        c = Computer([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        c.run([indata])
        assert c.output == [outdata]

    for indata, outdata in zip([7, 8, 9], [999, 1000, 1001]):
        c = Computer([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                      1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                      999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        c.run([indata])
        assert c.output == [outdata]

    puz = Puzzle(2019, 5)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
