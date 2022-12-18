def day18_part1(input):
    lava = set([tuple([int(y) for y in x.split(',')]) for x in input.split('\n')])
    surfaces = 0

    for (x, y, z) in lava:
        for (dx, dy, dz) in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            nx, ny, nz = x + dx, y + dy, z + dz
            surfaces += 1 if (nx, ny, nz) not in lava else 0
    return surfaces

def day18_part2(input):
    lava = set([tuple([int(y) for y in x.split(',')]) for x in input.split('\n')])
    

    # procedure: do a BFS from outside the lava to attain set of outside points
    # whilst doing this, we can count boundaries with the lava encountered

    xLocs, yLocs, zLocs = [a[0] for a in lava], [a[1] for a in lava], [a[2] for a in lava]
    xMin, xMax = min(xLocs) - 1, max(xLocs) + 1
    yMin, yMax = min(yLocs) - 1, max(yLocs) + 1
    zMin, zMax = min(zLocs) - 1, max(zLocs) + 1

    water = set([])
    frontier = [(xMin, yMin, zMin)]
    surfaces = 0

    while len(frontier) > 0:
        x, y, z = frontier.pop(0)
        if (x,y,z) in lava or (x,y,z) in water: continue
        if x < xMin or y < yMin or z < zMin: continue
        if x > xMax or y > yMax or z > zMax: continue
        
        water.add((x, y, z))
        for (dx, dy, dz) in ((-1, 0, 0), (1, 0, 0), (0, -1, 0), (0, 1, 0), (0, 0, -1), (0, 0, 1)):
            nx, ny, nz = x + dx, y + dy, z + dz
            surfaces += 1 if (nx, ny, nz) in lava else 0
            frontier.append((nx, ny, nz))

    return surfaces

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day18_part1(example_input) == 64
    print(day18_part1(test_input))

    assert day18_part2(example_input) == 58
    print(day18_part2(test_input))