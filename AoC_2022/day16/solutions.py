import re
import math
from itertools import permutations
from itertools import combinations

def parseInput(input):
    flow = {}
    tunnels = {}
    for line in input.split('\n'):
        splitLine = line.split()
        valve = splitLine[1]
        flow[valve] = int(re.findall(r'[-]?\d+', line)[0])
        tunnels[valve] = [x.replace(',', '') for x in splitLine[9:]]

    # find the shortest path length between every two valves using Floyd Warshall
    paths = {(a,b):0 if a == b else 1 if b in tunnels[a] else math.inf for a in tunnels for b in tunnels}
    for m in tunnels:
        new_paths = {}
        for i in tunnels:
            for j in tunnels:
                new_paths[(i, j)] = min(paths[(i, j)], paths[(i, m)] + paths[(m, j)])
        paths = new_paths

    return flow, paths

# globally tracking solutions for a given (time, valves) to optimise
memoization = {}

# calculates maximal pressure that can be released over time, optionally only using those in valves
def getMaxPressure(flow, dists, time, valves = None):
    valves = [x for x in flow if flow[x]>0] if valves is None else valves

    # if this (time, valves) combination has been encountered before, use saved solution
    if (time, frozenset(valves)) in memoization: return memoization[(time, frozenset(valves))]

    # filter down distances to if they connect two >0 caves or start from AA
    dists = {(a, b):v for ((a, b), v) in dists.items() if (flow[a]*flow[b]>0) or (a=='AA' and flow[b]>0)}
    flow = {x: flow[x] for x in valves if flow[x] > 0}
    
    # for pruning later: calculate total flow over all valves
    full_flow = sum(flow.values())
    
    # we will characterise a configuration as time left, current loc, open valves, current flow since start
    initialConfig = (time, 'AA', frozenset([]), 0)
    frontier = [initialConfig]
    come_from = {initialConfig: None}
    maxFinalFlow = 0
    final_state = None

    while len(frontier) > 0:
        (timeLeft, loc, openV, pastFlow) = curr_state = frontier.pop(0)
        # print(timeLeft, loc, openV, pastFlow)

        currFlow = sum([flow[x] for x in openV])
        nextCaves = [x for x in valves if x not in openV and timeLeft >= dists[(loc, x)] + 1]

        if len(nextCaves) == 0:
            # all >0 valves visited or not enough time left to visit more, calculate flow generated during remaining time
            newFlow = pastFlow + timeLeft * currFlow
            final_state = curr_state if newFlow > maxFinalFlow else final_state
            maxFinalFlow = max(newFlow, maxFinalFlow)
            continue

        if pastFlow + full_flow * timeLeft < maxFinalFlow:
            # even with maximal flow we can't beat the current best solution: prune this branch
            continue

        for nxt in nextCaves:
            newTimeLeft = timeLeft - dists[(loc, nxt)] - 1
            newFlow = pastFlow + currFlow * (dists[(loc, nxt)] + 1)
            new_state = (newTimeLeft, nxt, frozenset(openV.union([nxt])), newFlow)

            if new_state in come_from: continue
            come_from[new_state] = curr_state
            frontier.insert(0, new_state)

    # storing final solution for reuse, also if not all valves are visited
    memoization[(time, frozenset(valves))] = maxFinalFlow 
    memoization[(time, frozenset(final_state[2]))] = maxFinalFlow
    return maxFinalFlow

def day16_part1(input):
    flow, dists = parseInput(input)
    return getMaxPressure(flow, dists, 30)

def day16_part2(input, progress_bar = False):
    flow, dists = parseInput(input)

    # approach: for every subset a of the >0 valves we say we can visit these valves and the elephant can visit the remaining >0 valves
    # apply our part 1 solution over 26 seconds for both us and the elephant individually
    # since the two sets don't intersect, we can take their sum for the flow released overall
    valves = {x for x in flow if flow[x] > 0}
    valve_subsets = [set(v) for a in range(1, len(valves)) for v in combinations(valves, a)]
    checked = {} # (subset1, subset2) combinations checked to prevent (subset2, subset1) being checked unnecessarily 
    
    for i, hValves in enumerate(valve_subsets):
        eValves = valves.difference(hValves)
        hFrozen, eFrozen = frozenset(hValves), frozenset(eValves)
        if (eFrozen, hFrozen) in checked: continue

        # calculate combined flow and update progress bar
        checked[(hFrozen, eFrozen)] = getMaxPressure(flow, dists, 26, hValves) + getMaxPressure(flow, dists, 26, eValves)
        if progress_bar: printProgressBar(i, (len(valve_subsets)//2) - 1, prefix = 'Part 2 progress:', suffix = 'Complete', length = 50)

    return max(checked.values())

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration >= total: 
        print()

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day16_part1(example_input) == 1651
    print(day16_part1(test_input))

    assert day16_part2(example_input) == 1707
    print(day16_part2(test_input, True))