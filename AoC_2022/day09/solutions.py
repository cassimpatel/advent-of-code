from operator import add
from math import sqrt

def day9_part1(input):
    cmds = [[x.split()[0], int(x.split()[1])] for x in input.split('\n')]

    directions = {'U':[0, 1], 'D':[0, -1], 'L':[-1, 0], 'R':[1, 0]}
    H, T = [0, 0], [0, 0]
    TVisits = set(['0,0'])

    for [dir, num_spaces] in cmds:
        print(dir, num_spaces)
        for _ in range(num_spaces):
            H = list(map(add, H, directions[dir]))
            dist = sqrt((H[0]-T[0])**2 + (H[1]-T[1])**2)
            if dist <= sqrt(2): continue
            if dist > 2:
                # T must move diagonally
                if abs(H[1] - T[1]) == 2:
                    # two spaces north or south
                    T[1] += int((H[1] - T[1]) / 2)
                    T[0] += int((H[0] - T[0]) / 2)
                elif abs(H[0] - T[0]) == 2:
                    # two spaces east or west
                    T[0] += int((H[0] - T[0]) / 2)

            elif abs(H[1] - T[1]) == 2:
                # two spaces north or south
                T[1] += int((H[1] - T[1]) / 2)
            elif abs(H[0] - T[0]) == 2:
                # two spaces east or west
                T[0] += int((H[0] - T[0]) / 2)

            print('far away')
        print(H)


    print(directions)
    return None

def day9_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day9_part1(example_input) == 13
    print(day9_part1(test_input))

    # assert day9_part2(example_input) == 24933642
    # print(day9_part2(test_input))