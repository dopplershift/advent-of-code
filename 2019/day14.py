from collections import Counter


class Creator:
    def __init__(self, recipes):
        self.recipes = recipes
        self.inventory = Counter()

    @classmethod
    def fromfile(cls, fobj):
        recipes = {}
        for line in fobj:
            ingred, output = line.strip().split(' => ')
            out_count, out = output.split()
            inp = [((parts := i.split())[1], int(parts[0])) for i in ingred.split(', ')]
            recipes[out] = [int(out_count)] + inp
        return cls(recipes)

    def make(self, item, count):
        ore_count = 0

        prod_count, *ingreds = self.recipes[item]
        mult = count // prod_count + (count % prod_count > 0)

        for ingred, num in ingreds:
            if ingred == 'ORE':
                ore_count += mult * num
            else:
                if self.inventory[ingred] < mult * num:
                    ore_count += self.make(ingred, mult * num - self.inventory[ingred])
                self.inventory[ingred] -= mult * num

        self.inventory[item] += mult * prod_count

        return ore_count

    def max_for_ore(self, item, limit=1000000000000):
        lower = 1
        upper = limit
        guess = limit // self.make(item, 1) * 2
        while upper - lower > 1:
#            print(lower, upper, guess)
            ore = self.make(item, guess)
            if ore > limit:
                upper = guess
            elif ore < limit:
                lower = guess
            else:
                return guess
            guess = (lower + upper) // 2
        return lower


def run(data):
    c = Creator.fromfile(data.split('\n'))
    return c.make('FUEL', 1), c.max_for_ore('FUEL')


if __name__ == '__main__':
    from aocd.models import Puzzle

    c = Creator.fromfile("""10 ORE => 10 A
    1 ORE => 1 B
    7 A, 1 B => 1 C
    7 A, 1 C => 1 D
    7 A, 1 D => 1 E
    7 A, 1 E => 1 FUEL""".split('\n'))
    assert c.make('FUEL', 1) == 31

    c = Creator.fromfile("""9 ORE => 2 A
    8 ORE => 3 B
    7 ORE => 5 C
    3 A, 4 B => 1 AB
    5 B, 7 C => 1 BC
    4 C, 1 A => 1 CA
    2 AB, 3 BC, 4 CA => 1 FUEL""".split('\n'))
    assert c.make('FUEL', 1) == 165

    sample = '''157 ORE => 5 NZVS
    165 ORE => 6 DCFZ
    44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
    12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
    179 ORE => 7 PSHF
    177 ORE => 5 HKGWZ
    7 DCFZ, 7 PSHF => 2 XJWVT
    165 ORE => 2 GPVTF
    3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'''
    test_a, test_b = run(sample)
    assert test_a == 13312
    assert test_b == 82892753

    sample = '''2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
    17 NVRVD, 3 JNWZP => 8 VPVL
    53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
    22 VJHF, 37 MNCFX => 5 FWMGM
    139 ORE => 4 NVRVD
    144 ORE => 7 JNWZP
    5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
    5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
    145 ORE => 6 MNCFX
    1 NVRVD => 8 CXFTF
    1 VJHF, 6 MNCFX => 4 RFSQX
    176 ORE => 6 VJHF'''
    test_a, test_b = run(sample)
    assert test_a == 180697
    assert test_b == 5586022

    sample = '''171 ORE => 8 CNZTR
    7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
    114 ORE => 4 BHXH
    14 VRPVC => 6 BMBT
    6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
    6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
    15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
    13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
    5 BMBT => 4 WPTQ
    189 ORE => 9 KTJDG
    1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
    12 VRPVC, 27 CNZTR => 2 XDBXC
    15 KTJDG, 12 BHXH => 5 XCVML
    3 BHXH, 2 VRPVC => 7 MZWV
    121 ORE => 7 VRPVC
    7 XCVML => 6 RJRHP
    5 BHXH, 4 VRPVC => 5 LTCX'''
    test_a, test_b = run(sample)
    assert test_a == 2210736
    assert test_b == 460664

    puz = Puzzle(2019, 14)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
