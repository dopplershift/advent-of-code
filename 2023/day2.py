def parse(data):
    games = {}
    for line in data.split('\n'):
        game, pulls = line.lstrip().split(':')
        game_id = int(game.split()[-1])
        games[game_id] = [{(p := item.split())[-1]: int(p[0]) for item in pull.split(', ')}
                          for pull in pulls.split(';')]
    return games


def part1(games):
    total = 0
    for game_id, pulls in games.items():
        for marbles in pulls:
            if marbles.get('red', 0) > 12 or marbles.get('green', 0) > 13 or marbles.get('blue', 0) > 14:
                break
        else:
            total += game_id

    return total


def power(game):
    prod = 1
    for kind in ['red', 'green', 'blue']:
        prod *= max(m.get(kind, 0) for m in game)
    return prod


def part2(games):
    return sum(power(game) for game in games.values())


def run(data):
    games = parse(data)
    return part1(games), part2(games)


if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green'''

    test_a, test_b = run(sample)
    assert test_a == 8
    assert test_b == 2286

    puz = Puzzle(2023, 2)
    part_a, part_b = run(puz.input_data)

    puz.answer_a = part_a
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = part_b
    print(f'Part 2: {puz.answer_b}')
