def add(memory, r1, r2, r3):
    memory[r3] = memory[r1] + memory[r2]

def mul(memory, r1, r2, r3):
    memory[r3] = memory[r1] * memory[r2]

def halt(*a):
    raise StopIteration

dispatch = {1: add, 2:mul, 99: halt}
def run(program_memory):
    i_ptr = 0
    while i_ptr < len(program_memory):
        opcode = program_memory[i_ptr]
        try:
            dispatch[opcode](program_memory, *program_memory[i_ptr + 1:i_ptr + 4])
        except StopIteration:
            break
        i_ptr += 4
    return program_memory

if __name__ == '__main__':
    import itertools
    from aocd.models import Puzzle

    assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]
    assert run([1,0,0,0,99]) == [2,0,0,0,99]
    assert run([2,3,0,3,99]) == [2,3,0,6,99]
    assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
    assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]

    puz = Puzzle(2019, 2)
    codes = [int(c) for c in puz.input_data.split(',')]

    codes[1] = 12
    codes[2] = 2
    sol = run(codes)[0]
    puz.answer_a = sol
    print(f'Part 1: {puz.answer_a}')

    original_codes = [int(c) for c in puz.input_data.split(',')]

    for noun, verb in itertools.product(range(0, 100), range(0, 100)):
        codes = original_codes.copy()
        codes[1] = noun
        codes[2] = verb
        if run(codes)[0] == 19690720:
            break
    else:
        raise RuntimeError('No solution found!')

    sol = 100 * noun + verb
    puz.answer_b = sol
    print(f'Part 2: {puz.answer_b}')
