import itertools

from intcode import Computer


def run(data):
    code = [int(c) for c in data.split(',')]
    return find_max_thrust(code)[-1], find_max_thrust_feedback(code)[-1]


def find_max_thrust(code):
    max_thrust = 0
    for phases in itertools.permutations(range(5), 5):
        val = 0
        for phase in phases:
            c = Computer(code)
            c.run([phase, val])
            val = c.output[0]
        if c.output[0] > max_thrust:
            max_thrust = c.output[0]
            best = phases
    return best, max_thrust


def find_max_thrust_feedback(code):
    max_thrust = 0
    for phases in itertools.permutations(range(5, 10), 5):
        amps = [Computer(code, id=i) for i in range(5)]
        for i, (phase, amp) in enumerate(zip(phases, amps)):
            amps[i-1].connect_sink(amp)
            amp.send_input([phase])

        amps[0].send_input([0])

        while any(amp.running for amp in amps):
            for amp in amps:
                amp.run()

        if amps[-1].output[0] > max_thrust:
            max_thrust = amps[-1].output[0]
            best = phases
    return best, max_thrust


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert find_max_thrust([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0]) == ((4, 3, 2, 1, 0), 43210)
    assert (find_max_thrust([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
            == ((0, 1, 2, 3, 4), 54321))
    assert (find_max_thrust([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
            == ((1, 0, 4, 3, 2), 65210))

    assert (find_max_thrust_feedback([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
            == ((9, 8, 7, 6, 5), 139629729))
    assert (find_max_thrust_feedback([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
                                      -5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
                                      53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
            == ((9, 7, 8, 5, 6), 18216))

    puz = Puzzle(2019, 7)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
