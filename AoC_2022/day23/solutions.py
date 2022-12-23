def getElves(input):
    input = [[y for y in x] for x in input.split('\n')]
    elves = set([])
    for y in range(len(input)):
        for x in range(len(input[0])):
            if input[y][x] == '.': continue
            elves.add((x, y))
    return elves
    
def day23_part1(input):
    elves = getElves(input)
    
    neighbours = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    dirs = [
        [(0, -1), (1, -1), (-1, -1)],
        [(0, 1), (1, 1),  (-1, 1)],
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0),  (1, 1),  (1, -1)]
    ]

    for _ in range(10):
        # print(elves)
        proposed = {}
        for (x, y) in elves:
            e_neighbours = {(dx, dy):(x+dx, y+dy) in elves for (dx, dy) in neighbours}

            if list(e_neighbours.values()).count(False) == 8:
                continue
            for dir in dirs:
                checks = [e_neighbours[x] for x in dir]
                if checks.count(False) == 3:
                    dx, dy = dir[0]
                    proposed[(x, y)] = (x+dx, y+dy)
                    # print(x, y, x+dx, y+dy)
                    break
        proposed_locs = list(proposed.values())
        proposed = {x:y for (x, y) in proposed.items() if proposed_locs.count(y) == 1}
        elves = {proposed[x] if x in proposed else x for x in elves}
        dirs.append(dirs.pop(0))
    
    x, y = set([x for (x, y) in elves]), set([y for (x, y) in elves])
    min_x, max_x = min(x), max(x)
    min_y, max_y = min(y), max(y)
            
    return (abs(max_x - min_x + 1) * abs(max_y - min_y + 1)) - len(elves)

def day23_part2(input):
    elves = getElves(input)
    
    neighbours = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))
    dirs = [
        [(0, -1), (1, -1), (-1, -1)],
        [(0, 1), (1, 1),  (-1, 1)],
        [(-1, 0), (-1, 1), (-1, -1)],
        [(1, 0),  (1, 1),  (1, -1)]
    ]

    rounds = 0

    while True:
        # print(elves)
        proposed = {}
        for (x, y) in elves:
            e_neighbours = {(dx, dy):(x+dx, y+dy) in elves for (dx, dy) in neighbours}

            if list(e_neighbours.values()).count(False) == 8:
                continue
            for dir in dirs:
                checks = [e_neighbours[x] for x in dir]
                if checks.count(False) == 3:
                    dx, dy = dir[0]
                    proposed[(x, y)] = (x+dx, y+dy)
                    # print(x, y, x+dx, y+dy)
                    break
        proposed_locs = list(proposed.values())
        proposed = {x:y for (x, y) in proposed.items() if proposed_locs.count(y) == 1}
        elves = {proposed[x] if x in proposed else x for x in elves}
        dirs.append(dirs.pop(0))
        rounds += 1
        if proposed == {}: break
    return rounds

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day23_part1(example_input) == 110
    print(day23_part1(test_input))

    assert day23_part2(example_input) == 20
    print(day23_part2(test_input))