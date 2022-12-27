# returns new rock location and whether or not it has moved
def move_rock(chamber, rock, dir):
    dirs = {'<':(-1, 0), '>':(1, 0), 'v':(0, -1)}
    dx, dy = dirs[dir]

    x = [x for (x, y) in rock]
    minX, maxX = min(x), max(x)

    newRock = []

    if dir == '<' and minX == 0: return rock, False
    if dir == '>' and maxX == 6: return rock, False

    for (x, y) in rock:
        nx, ny = x + dx, y + dy
        if (nx, ny) in chamber: return rock, False
        newRock.append((nx, ny))

    return newRock, True
    
def day17_part1(input):
    jets = [x for x in input]
    rocks = [
        [(2, 0), (3, 0), (4, 0), (5, 0)],
        [(2, 1), (3, 0), (3, 1), (3, 2), (4, 1)],
        [(2, 0), (3, 0), (4, 0), (4, 1), (4, 2)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
        [(2, 0), (2, 1), (3, 0), (3, 1)]
    ]
    chamber = set([(x, 0) for x in range(7)])

    jet = 0
    maxHeight = 0

    for i in range(2022):
        currRock = [(x, maxHeight + 4 + y) for (x, y) in rocks[i % len(rocks)]]
        settled = False

        while not settled:
            currJet = jets[jet]
            
            currRock, _ = move_rock(chamber, currRock, currJet)
            currRock, moved = move_rock(chamber, currRock, 'v')

            if not moved:
                settled = True
                chamber.update(currRock)
                maxHeight = max(maxHeight, max([y for (x, y) in currRock]))

            jet = (jet + 1) % len(jets)
    return maxHeight

def day17_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day17_part1(example_input) == 3068
    print(day17_part1(test_input))

    # assert day17_part2(example_input) == 1514285714288
    # print(day17_part2(test_input)