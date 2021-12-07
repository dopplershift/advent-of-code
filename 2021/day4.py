def parse(s):
    lines = s.split('\n')
    nums = list(map(int, lines[0].split(',')))
    boards = [list(map(int, (' '.join(lines[i:i + 6])).split()))
              for i in range(1, len(lines), 6)]
    return nums, boards


def winner(board, nums, n=5):
    return (any(set(board[i::5]) <= nums for i in range(5)) or 
            any(set(board[5*i:5 * i + 5]) <= nums for i in range(5)))


def score(board, nums):
    return nums[-1] * sum(set(board) - set(nums))


def find_winner(boards, all_nums):
    sofar = all_nums[:5]
    for num in all_nums[5:]:
        sofar.append(num)
        for board in boards:
            if winner(board, set(sofar)):
                return score(board, sofar)


def find_loser(boards, all_nums):
    sofar = all_nums[:5]
    for num in all_nums[5:]:
        sofar.append(num)
        if len(boards) >= 2:
            boards = [board for board in boards
                      if not winner(board, set(sofar))]
        if winner(boards[0], set(sofar)):
            break
    
    return score(boards[0], sofar)

if __name__ == '__main__':
    from aocd.models import Puzzle

    sample = '''7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7'''

    n, boards = parse(sample)
    assert find_winner(boards, n) == 4512
    assert find_loser(boards, n) == 1924

    puz = Puzzle(2021, 4)
    n, boards = parse(puz.input_data)

    puz.answer_a = find_winner(boards, n)
    print(f'Part 1: {puz.answer_a}')

    puz.answer_b = find_loser(boards, n)
    print(f'Part 2: {puz.answer_b}')