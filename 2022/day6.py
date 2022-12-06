def marker(s, l):
    for i in range(len(s) - l):
        if len(set(s[i:i+l])) == l:
            return i + l


def run(data):
    return marker(data, 4), marker(data, 14)


if __name__ == '__main__':
    from aocd.models import Puzzle

    assert marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 4) == 7
    assert marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 4) == 5
    assert marker('nppdvjthqldpwncqszvftbrmjlhg', 4) == 6
    assert marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 4) == 10
    assert marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 4) == 11

    assert marker('mjqjpqmgbljsphdztnvjfqwrcgsmlb', 14) == 19
    assert marker('bvwbjplbgvbhsrlpgdmjqwftvncz', 14) == 23
    assert marker('nppdvjthqldpwncqszvftbrmjlhg', 14) == 23
    assert marker('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 14) == 29
    assert marker('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 14) == 26

    puz = Puzzle(2022, 6)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
