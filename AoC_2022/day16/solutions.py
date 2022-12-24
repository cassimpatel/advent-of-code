import re
import math
from queue import PriorityQueue

def parseInput(input):
    flow = {}
    tunnels = {}
    for line in input.split('\n'):
        splitLine = line.split()
        valve = splitLine[1]
        flow[valve] = int(re.findall(r'[-]?\d+', line)[0])
        tunnels[valve] = [x.replace(',', '') for x in splitLine[9:]]
    return flow, tunnels

# finds the shortest path length between every two valves using Floyd Warshall
def shortestPaths(tunnels):
    # initialise paths lengths as 1 if connected, 0 to self, infinity otherwise
    paths = {(a,b):0 if a == b else 1 if b in tunnels[a] else math.inf for a in tunnels for b in tunnels}

    for m in tunnels:
        new_paths = {}
        for i in tunnels:
            for j in tunnels:
                new_paths[(i, j)] = min(paths[(i, j)], paths[(i, m)] + paths[(m, j)])
        paths = new_paths

    return paths

def day16_part1(input):
    flow, tunnels = parseInput(input)
    dists = shortestPaths(tunnels)

    # filter down distances to if they connect two >0 caves or start from AA
    dists = {(a, b):v for ((a, b), v) in dists.items() if (flow[a]*flow[b]>0) or (a=='AA' and flow[b]>0)}
    flow = {x: flow[x] for x in flow if flow[x] > 0}

    # we will characterise a configuration as time left, current loc, open valves, current flow since start
    initialConfig = (30, 'AA', set([]), 0)
    frontier = [initialConfig]
    maxFinalFlow = 0
    
    while len(frontier) > 0:
        (timeLeft, loc, openV, pastFlow) = frontier.pop(0)
        # print(timeLeft, loc, openV, pastFlow)

        currFlow = sum([flow[x] for x in openV])
        nextCaves = [x for x in flow if x not in openV and timeLeft >= dists[(loc, x)] + 1]

        if len(nextCaves) == 0:
            # all >0 valves visited or not enough time left to visit more, calculate flow generated during remaining time
            newFlow = pastFlow + timeLeft * currFlow
            maxFinalFlow = max(newFlow, maxFinalFlow)
            continue

        for nxt in nextCaves:
            newTimeLeft = timeLeft - dists[(loc, nxt)] - 1
            newFlow = pastFlow + currFlow * (dists[(loc, nxt)] + 1)
            frontier.insert(0, (newTimeLeft, nxt, openV.union([nxt]), newFlow))

    return maxFinalFlow

def day16_part2(input):
    # approach: similar to part 1 but include the elephants loc as another parameter
    # additionally decrease time left on start state to 26
    # elephant and self can reach their destinations in different times so track time remaining for both to get to their next goal in the state (whichever comes first, remove same time from the max one too)
    # when considering which cave to go to next, try all choices for both
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day16_part1(example_input) == 1651
    print(day16_part1(test_input))

    assert day16_part2(example_input) == 1707
    # print(day16_part2(test_input)