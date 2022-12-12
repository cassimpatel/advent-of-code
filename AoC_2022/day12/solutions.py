# Conducting a search from E to S
# If goal is None, we find the cost to the closest height 1 location
def breadth_first_search(graph, start, goal=None):
    frontier = [start]
    cost = {start:0}

    gridH = len(graph)
    gridW = len(graph[0])
    elevation = {chr(x):x-96 for x in range(97, 123)} | {'S':1, 'E':26}
    
    while len(frontier) > 0:
        current = frontier.pop(0)
        y, x = current
        
        if current == goal or (goal is None and elevation[graph[y][x]] == 1):
            goal = current
            break

        for (dy, dx) in ((0, 1), (0, -1), (-1, 0), (1, 0)):
            newX, newY = x + dx, y + dy

            if newX in [-1, gridW] or newY in [-1, gridH]: continue
            if elevation[graph[y][x]] > elevation[graph[newY][newX]] + 1: continue
            if (newY, newX) in cost: continue

            neighbour = (newY, newX)
            cost[neighbour] = cost[current] + 1
            frontier.append(neighbour)

    return cost[goal]

def day12_part1(input):
    grid = [[y for y in x] for x in input.split('\n')]

    sLoc = [(index, row.index('S')) for index, row in enumerate(grid) if 'S' in row][0]
    eLoc = [(index, row.index('E')) for index, row in enumerate(grid) if 'E' in row][0]
    cost = breadth_first_search(grid, eLoc, sLoc)

    return cost

def day12_part2(input):
    grid = [[y for y in x] for x in input.split('\n')]

    eLoc = [(index, row.index('E')) for index, row in enumerate(grid) if 'E' in row][0]
    cost = breadth_first_search(grid, eLoc, None)

    return cost

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day12_part1(example_input) == 31
    print(day12_part1(test_input))

    assert day12_part2(example_input) == 29
    print(day12_part2(test_input))