from queue import PriorityQueue

def parse_input(input):
    grid = [[y for y in x] for x in input.split('\n')]
    w, h = len(grid[0]), len(grid)

    dirs = {'^':(0, -1), '<':(-1, 0), '>':(1, 0), 'v':(0, 1)}

    # for every tile: timesteps (over w or h) where a blizzard exists (this loops over w or h respectively)
    blizzard_timestep = {(x, y, d): set([]) for x in range(w) for y in range(h) for d in ['x', 'y']}

    # for each blizzard, we move in its direction till it loops, marking the relative timestep each tile is affected
    # this should let us quickly look at a tile to find if it is affected during a given timestep
    for y in range(1, h-1):
        for x in range(1, w-1):
            if grid[y][x] == '.': continue
            dx, dy = dirs[grid[y][x]]
            nx, ny = x, y

            time_step = 0
            while True:
                # depending on the direction of the blizzard set timestep differently (as w and h have different lengths)
                XorY = 'x' if grid[y][x] in ['<', '>'] else 'y'
                blizzard_timestep[(nx, ny, XorY)].add(time_step)
                
                # increment by dx and dy, then map back to the traversable area in the grid
                nx, ny = ((nx + dx - 1) % (w - 2)) + 1, ((ny + dy - 1) % (h - 2)) + 1
                if (nx, ny) == (x, y): break
                time_step += 1

    return (grid, blizzard_timestep)

# searches given start state (x, y, timestep), end location (ex, ey), grid, blizzard tile timesteps
# returns the final state (ex, ey, timestep) using A*
def search(startState, endLoc, grid, blizzard_timesteps):
    w, h = len(grid[0]), len(grid)
    ex, ey = endLoc

    visited_states = set([])
    frontier = PriorityQueue()
    frontier.put((0, startState))

    while not frontier.empty():
        (priority, currState) = frontier.get()
        (x, y, time_step) = currState
        # print(x, y, time_step)

        if (x, y) == endLoc:
            return currState
        
        if currState in visited_states: continue
        visited_states.add((x, y, time_step))
        
        # we can either down, up, right, up or wait
        for (dx, dy) in ((0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)):
            nx, ny = x + dx, y + dy

            # if the tile is a wall or will occupy a blizzard: don't consider it
            if ny < 0 or ny >= h or grid[ny][nx] == '#': continue
            xTimes, yTimes = blizzard_timesteps[(nx, ny, 'x')], blizzard_timesteps[(nx, ny, 'y')]
            if (time_step + 1) % (w - 2) in xTimes or (time_step + 1) % (h - 2) in yTimes: continue

            # calculate cost as one more than current, and use manhattan distance heuristic
            new_cost = time_step + 1
            heuristic = abs(ex-nx) + abs(ey-ny)
            priority = new_cost + heuristic

            frontier.put((priority, (nx, ny, new_cost)))
    
    return 'SOLUTION NOT FOUND'

def day24_part1(input):
    grid, blizzard_timesteps = parse_input(input)
    w, h = len(grid[0]), len(grid)

    # state given x, y, current_timesteps
    startState = (1, 0, 0)
    endLoc = (w-2, h-1)

    endState = search(startState, endLoc, grid, blizzard_timesteps)
    (endX, endY, timesteps) = endState
    return timesteps

def day24_part2(input):
    grid, blizzard_timesteps = parse_input(input)
    w, h = len(grid[0]), len(grid)

    # state given x, y, current_timesteps
    startState = (1, 0, 0)
    startLoc, endLoc = (1, 0), (w-2, h-1)

    # travel to endLoc then to startLoc then back to endLoc, preserving the end state to reuse
    endState = search(startState, endLoc,   grid, blizzard_timesteps)
    endState = search(endState,   startLoc, grid, blizzard_timesteps)
    endState = search(endState,   endLoc,   grid, blizzard_timesteps)

    (endX, endY, timesteps) = endState
    return timesteps

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day24_part1(example_input) == 18
    print(day24_part1(test_input))

    assert day24_part2(example_input) == 54
    print(day24_part2(test_input))