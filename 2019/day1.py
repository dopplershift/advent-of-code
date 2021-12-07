from aocd.models import Puzzle

def total_fuel(mass):
    total = 0
    while mass:
        mass = max(mass // 3 - 2, 0)
        total += mass
    return total

puz = Puzzle(2019, 1)

assert total_fuel(14) == 2
assert total_fuel(1969) == 966
assert total_fuel(100756) == 50346

vals = list(map(int, puz.input_data.split('\n')))

total = sum(i // 3 - 2 for i in vals)
puz.answer_a = total
print(f'Part 1: {puz.answer_a}')

total = sum(total_fuel(i) for i in vals)
puz.answer_b = total
print(f'Part 2: {puz.answer_b}')
