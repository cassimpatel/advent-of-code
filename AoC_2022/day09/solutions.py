from operator import add
from math import sqrt

def day9_part1(input):
    cmds = [[x.split()[0], int(x.split()[1])] for x in input.split('\n')]

    directions = {'U':[0, 1], 'D':[0, -1], 'L':[-1, 0], 'R':[1, 0]}
    TVisits = set([])

    H, T = [0, 0], [0, 0]
    
    for [dir, num_spaces] in cmds:
        # print(dir, num_spaces)

        for _ in range(num_spaces):
            H = list(map(add, H, directions[dir]))

            dx, dy = H[0] - T[0], H[1] - T[1]

            if abs(dx) == 2:
                T[0], T[1] = H[0] - int(dx / 2), H[1]
            elif abs(dy) == 2:
                T[0], T[1] = H[0], H[1] - int(dy / 2)

            TVisits.add(str(T))

    return len(TVisits)

def day9_part2(input):
    cmds = [[x.split()[0], int(x.split()[1])] for x in input.split('\n')]

    directions = {'U':[0, 1], 'D':[0, -1], 'L':[-1, 0], 'R':[1, 0]}
    TVisits = set([])

    # Using Knots to denote the entire rope, where Knots[0] is now H
    Knots = {a:[0,0].copy() for a in range(10)}
    
    for [dir, num_spaces] in cmds:
        # print(dir, num_spaces)

        for _ in range(num_spaces):
            Knots[0] = list(map(add, Knots[0], directions[dir]))

            for currKnot in range(1, 10):
                # set current knots data to H and T
                H = Knots[currKnot - 1]
                T = Knots[currKnot].copy()
                dx, dy = H[0] - T[0], H[1] - T[1]

                # extra condition as complexity means dx and dy can both equal 2
                if abs(dx) == 2 and abs(dy) == 2:
                    T[0], T[1] = H[0] - int(dx / 2), H[1] - int(dy / 2)
                elif abs(dx) == 2:
                    T[0], T[1] = H[0] - int(dx / 2), H[1]
                elif abs(dy) == 2:
                    T[0], T[1] = H[0], H[1] - int(dy / 2)
                else:
                    # if the knot has not moved, the rest won't move: break
                    break
                Knots[currKnot] = T

            TVisits.add(str(Knots[9]))
    
    return len(TVisits)

if __name__ == "__main__":
    example1_input = open('example1.txt', 'r').read()
    example2_input = open('example2.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day9_part1(example1_input) == 13
    print(day9_part1(test_input))

    assert day9_part2(example1_input) == 1
    assert day9_part2(example2_input) == 36
    print(day9_part2(test_input))