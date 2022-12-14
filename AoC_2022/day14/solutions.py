def getRocksSet(input):
    input = [[[int(z) for z in y.split(',')] for y in x.split(' -> ')] for x in input.split('\n')]
    rocks = set([])

    for rockOrdering in input:
        x, y = rockOrdering[0]
        rocks.add((x, y))
        for [x1, y1] in rockOrdering[1:]:
            rockLine = [(a, b) for a in range(min(x, x1), max(x, x1)+1) for b in range(min(y, y1), max(y, y1)+1)]
            rocks.update(rockLine)
            x, y = x1, y1
    return rocks
    
def day14_part1(input):
    rocks = getRocksSet(input)
    sand = set([])
    lowestY = max([y for (x, y) in rocks])

    while True:
        x, y = 500, 0

        while True:
            moved = False
            for (dx, dy) in ((0, 1), (-1, 1), (1, 1)):
                newX, newY = x + dx, y + dy
                if (newX, newY) in rocks or (newX, newY) in sand: continue
                moved = True
                break

            if not moved:
                sand.add((x, y))
                break
            x, y = newX, newY
            if y >= lowestY: break
        if y >= lowestY: break

    return len(sand)

def day14_part2(input):
    rocks = getRocksSet(input)
    sand = set([(500, 0)])
    lowestY = max([y for (x, y) in rocks])
    
    # we don't have to worry about sand falling off the edge
    # hence we can do a simple BFS from the source upto maxY + 1
    frontier = [(500, 0)]
    
    while len(frontier) > 0:
        x, y = frontier.pop(0)
        for (dx, dy) in ((0, 1), (-1, 1), (1, 1)):
            newX, newY = x + dx, y + dy
            if (newX, newY) in rocks or (newX, newY) in sand or newY > lowestY + 1: continue
            sand.add((newX, newY))
            frontier.append((newX, newY))

    return len(sand)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day14_part1(example_input) == 24
    print(day14_part1(test_input))

    assert day14_part2(example_input) == 93
    print(day14_part2(test_input))