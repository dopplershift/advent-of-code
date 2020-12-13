from dataclasses import dataclass, field
import re
from typing import List


@dataclass
class Group:
    initiative: int
    hit_points: int
    units: int
    attack: int
    attack_type: str
    weaknesses: List[str] = field(default_factory=list)
    immunities: List[str] = field(default_factory=list)
    
    def __hash__(self):
        return self.initiative

    @property
    def power(self):
        return self.units * self.attack

    
parser = re.compile(r'(\d+) units each with (\d+) hit points( \([a-z ,;]*\))? with an attack that does (\d+) (\w+) damage at initiative (\d+)')

def parse_special(s):
    s = s[2:-1]
    weak = []
    immune = []
    while s:
        if ';' in s:
            ind = s.index(';')
            src = s[:ind]
            s = s[ind + 2:]
        else:
            src = s
            s = ''

        if src.startswith('weak'):
            weak = src[8:].split(', ')
        else:
            immune = src[10:].split(', ')

    return weak, immune


def parse(s):
    lines = iter(s.split('\n'))
    immune = []
    next(lines)
    for line in lines:
        if not line.rstrip():
            break
        pieces = parser.match(line.rstrip()).groups()
        immune.append(Group(int(pieces[-1]), int(pieces[1]), int(pieces[0]), int(pieces[3]), pieces[4]))
        if pieces[2] is not None:
            weak, strong = parse_special(pieces[2])
            immune[-1].weaknesses = weak
            immune[-1].immunities = strong

    infection = []
    next(lines)
    for line in lines:
        if not line.rstrip():
            break
        pieces = parser.match(line.rstrip()).groups()
        infection.append(Group(int(pieces[-1]), int(pieces[1]), int(pieces[0]), int(pieces[3]), pieces[4]))
        if pieces[2] is not None:
            weak, strong = parse_special(pieces[2])
            infection[-1].weaknesses = weak
            infection[-1].immunities = strong

    return immune, infection


def damage(attacker, defender):
    base = attacker.power
    if attacker.attack_type in defender.weaknesses:
        base *= 2
    elif attacker.attack_type in defender.immunities:
        base = 0
    return base


def select_targets(attackers, defenders):
    targets = dict()
    remaining = set(defenders)
    for group in sorted(attackers, key=lambda g: (g.power, g.initiative))[::-1]:
        if not remaining:
            break
        target = max(remaining, key=lambda d: (damage(group, d), d.power, d.initiative))
        if damage(group, target) != 0:
            targets[group] = target
            remaining.remove(target)
    return targets


def attack(groups, targets):
    for g in reversed(sorted(groups, key=lambda g: g.initiative)):
        if g.units > 0 and g in targets:
            target = targets[g]
            killed = min(damage(g, target) // target.hit_points, target.units)
#             print(g.initiative, damage(g, target), g.units, target.units, killed)
            target.units -= killed

    
def loop(immune, infection, boost=0):
    for i in immune:
        i.attack += boost
    while immune and infection:
        targets = {**select_targets(immune, infection), **select_targets(infection, immune)}
#         print(targets)
        attack(immune + infection, targets)
#         print(immune, infection)
        immune = [i for i in immune if i.units > 0]
        infection = [i for i in infection if i.units > 0]
    return immune, infection


if __name__ == '__main__':
    from aocd.models import Puzzle

    f = '''Immune System:
17 units each with 5390 hit points (weak to radiation, bludgeoning) with an attack that does 4507 fire damage at initiative 2
989 units each with 1274 hit points (immune to fire; weak to bludgeoning, slashing) with an attack that does 25 slashing damage at initiative 3

Infection:
801 units each with 4706 hit points (weak to radiation) with an attack that does 116 bludgeoning damage at initiative 1
4485 units each with 2961 hit points (immune to radiation; weak to fire, cold) with an attack that does 12 slashing damage at initiative 4'''

    immune, infection = parse(f)
    im, inf = loop(immune, infection)
    assert sum(g.units for g in im + inf) == 5216

    immune, infection = parse(f)
    im, inf = loop(immune, infection, 1570)
    assert sum(g.units for g in im + inf) == 51

    puz = Puzzle(2018, 24)
    immune, infection = parse(puz.input_data)
    im, inf = loop(immune, infection)
    puz.answer_a = sum(g.units for g in im + inf)
    print(f'Part 1: {puz.answer_a}')

    for boost in range(0, 3000):
        immune, infection = parse(f)
        im, inf = loop(immune, infection, boost)
        if im:
            break
    puz.anwer_b = sum(g.units for g in im + inf)
    print(f'Part 2: {puz.answer_b}')