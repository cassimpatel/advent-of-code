def day8_part1(input):
    trees = [[int(y) for y in x] for x in input.split('\n')]
    gridW = len(trees[0])
    gridH = len(trees)

    # up and down switched to manage array indexing visually increases downwards
    dir_vect = {'D':[0, 1], 'U':[0, -1], 'L':[-1, 0], 'R':[1, 0]}
    numVisibile = (gridH * 2) + (gridW - 2) * 2

    # for each tree in the forest
    for y in range(1, gridH - 1):
        for x in range(1,  gridW - 1):

            # print(y, x, trees[y][x])
            visible = False

            # for each dir, traverse in that direction
            # if reach and edge mark as visible, otherwise break if reach taller tree
            for dir in dir_vect:
                [dx, dy] = dir_vect[dir]
                mult = 1

                while not visible:
                    newX, newY = x + mult * dx, y + mult * dy
                    # print('curr', newY, newX)
                    if newX in [-1, gridW] or newY in [-1, gridH]:
                        visible = True
                    elif trees[newY][newX] >= trees[y][x]:
                        break
                    mult += 1
                
                if visible: break
            if visible: numVisibile += 1

    return numVisibile

def day8_part2(input):
    trees = [[int(y) for y in x] for x in input.split('\n')]
    gridW = len(trees[0])
    gridH = len(trees)

    # up and down switched to manage array indexing visually increases downwards
    dir_vect = {'D':[0, 1], 'U':[0, -1], 'L':[-1, 0], 'R':[1, 0]}
    maxScore = 0

    # for each tree in the forest
    for y in range(1, gridH - 1):
        for x in range(1,  gridW - 1):
            
            # print(y, x, trees[y][x])
            score = 1

            # for each dir, traverse in that direction
            # if reach and edge or taller tree break
            for dir in dir_vect:
                [dx, dy] = dir_vect[dir]
                mult = 1

                while True:
                    newX, newY = x + mult * dx, y + mult * dy
                    # print('curr', newY, newX)
                    if newX in [0, gridW-1] or newY in [0, gridH-1]:
                        break
                    elif trees[newY][newX] >= trees[y][x]:
                        break
                    mult += 1

                score *= mult
            maxScore = max(maxScore, score)

    return maxScore

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day8_part1(example_input) == 21
    print(day8_part1(test_input))

    assert day8_part2(example_input) == 8
    print(day8_part2(test_input))