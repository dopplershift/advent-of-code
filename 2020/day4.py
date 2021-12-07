import re


def parse(s):
    passports = s.split('\n\n')
    for p in passports:
        fields = p.split()
        d = {}
        for field in fields:
            key,value = field.split(':')
            d[key] = value
        yield d


def validate_height(s):
    if s.endswith('cm'):
        return 150 <= int(s[:-2]) <= 193
    elif s.endswith('in'):
        return 59 <= int(s[:-2]) <= 76
    else:
        return False


def validate_eye_color(s):
    return s in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


required = {'byr': lambda v: 1920 <= int(v) <= 2002,
            'iyr': lambda v: 2010 <= int(v) <= 2020,
            'eyr': lambda v: 2020 <= int(v) <= 2030,
            'hgt': validate_height,
            'hcl': lambda v: re.match('#[0-9a-f]{6}', v) is not None,
            'ecl': validate_eye_color,
            'pid': lambda v: re.match('^\d{9}$', v) is not None} # 'cid'


def validate1(passport):
    return all(f in passport for f in required)


def validate2(passport):
    return all(f in passport and required[f](passport[f]) for f in required)


if __name__ == '__main__':
    from aocd.models import Puzzle

    test_input = '''ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
    byr:1937 iyr:2017 cid:147 hgt:183cm

    iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
    hcl:#cfa07d byr:1929

    hcl:#ae17e1 iyr:2013
    eyr:2024
    ecl:brn pid:760753108 byr:1931
    hgt:179cm

    hcl:#cfa07d eyr:2025 pid:166559648
    iyr:2011 ecl:brn hgt:59in'''

    data = list(parse(test_input))

    assert sum(validate1(p) for p in data) == 2

    test_input = '''eyr:1972 cid:100
    hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

    iyr:2019
    hcl:#602927 eyr:1967 hgt:170cm
    ecl:grn pid:012533040 byr:1946

    hcl:dab227 iyr:2012
    ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

    hgt:59cm ecl:zzz
    eyr:2038 hcl:74454a iyr:2023
    pid:3556412378 byr:2007'''
    data = list(parse(test_input))
    assert sum(validate2(p) for p in data) == 0

    test_input = '''pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
    hcl:#623a2f

    eyr:2029 ecl:blu cid:129 byr:1989
    iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

    hcl:#888785
    hgt:164cm byr:2001 iyr:2015 cid:88
    pid:545766238 ecl:hzl
    eyr:2022

    iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719'''
    data = list(parse(test_input))
    assert sum(validate2(p) for p in data) == 4

    puz = Puzzle(2020, 4)
    data = list(parse(puz.input_data))

    puz.answer_a = sum(validate1(p) for p in data)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = sum(validate2(p) for p in data)
    print(f'Part 2: {puz.answer_b}')
