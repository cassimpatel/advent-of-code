def day2_part1(input):
    move_dict = {'A':1, 'B':2, 'C':3, 'X':1, 'Y':2, 'Z':3}

    input = [x.split(' ') for x in input.split('\n')]
    input = [[move_dict[x[0]], move_dict[x[1]]] for x in input]

    score = 0
    for [opponent_move, me_move] in input:
        score += me_move

        if me_move == opponent_move:
            score += 3
        elif (me_move - opponent_move) % 3 == 1:
            score += 6

    return score

def day2_part2(input):
    move_dict = {'A':1, 'B':2, 'C':3, 'X':0, 'Y':3, 'Z':6}

    input = [x.split(' ') for x in input.split('\n')]
    input = [[move_dict[x[0]], move_dict[x[1]]] for x in input]

    score = 0
    for [opponent_move, outcome] in input:
        score += outcome

        # we can calculate the int offset from opponent_move using the outcome for our move
        offset = (outcome / 3) - 1
        score += ((opponent_move -1 + offset) % 3) + 1

    return int(score)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day2_part1(example_input) == 15 
    print(day2_part1(test_input))

    # assert day2_part2(example_input) == 12
    print(day2_part2(test_input))