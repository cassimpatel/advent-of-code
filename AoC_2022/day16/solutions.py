import re
import math
from queue import PriorityQueue
from itertools import permutations

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
    # for pruning later: calculate total flow over all valves
    full_flow = sum(flow.values())

    # we will characterise a configuration as time left, current loc, open valves, current flow since start
    initialConfig = (30, 'AA', frozenset([]), 0)
    frontier = [initialConfig]
    come_from = {initialConfig: None}
    maxFinalFlow = 0

    while len(frontier) > 0:
        (timeLeft, loc, openV, pastFlow) = curr_state = frontier.pop(0)
        # print(timeLeft, loc, openV, pastFlow)

        currFlow = sum([flow[x] for x in openV])
        nextCaves = [x for x in flow if x not in openV and timeLeft >= dists[(loc, x)] + 1]

        if len(nextCaves) == 0:
            # all >0 valves visited or not enough time left to visit more, calculate flow generated during remaining time
            newFlow = pastFlow + timeLeft * currFlow
            maxFinalFlow = max(newFlow, maxFinalFlow)
            continue

        if pastFlow + full_flow * timeLeft < maxFinalFlow:
            continue

        for nxt in nextCaves:
            newTimeLeft = timeLeft - dists[(loc, nxt)] - 1
            newFlow = pastFlow + currFlow * (dists[(loc, nxt)] + 1)
            new_state = (newTimeLeft, nxt, frozenset(openV.union([nxt])), newFlow)

            if new_state in come_from: continue
            come_from[new_state] = curr_state
            frontier.insert(0, new_state)

    return maxFinalFlow

def day16_part2(input):
    # approach: similar to part 1 but include the elephants loc as another parameter
    # additionally decrease time left on start state to 26
    # elephant and self can reach their destinations in different times so track time remaining for both to get to their next goal in the state (whichever comes first, remove same time from the max one too)
    # when considering which cave to go to next, try all choices for both


    flow, tunnels = parseInput(input)
    dists = shortestPaths(tunnels)

    # filter down distances to if they connect two >0 caves or start from AA
    dists = {(a, b):v for ((a, b), v) in dists.items() if (flow[a]*flow[b]>0) or (a=='AA' and flow[b]>0)}
    flow = {x: flow[x] for x in flow if flow[x] > 0}

    # we will characterise a configuration as time left, my goal valve, elephant goal valve, time till I reach my valve, time till elephant reaches its valve, open valves, past flow
    initialConfig = (26, 'AA', 'AA', 0, 0, set([]), 0)
    frontier = [initialConfig]
    maxFinalFlow = 0


    visited_states = set([])
    come_from = {(26, 'AA', 'AA', 0, 0, frozenset(set([])), 0): None}
    final_state = None

    num_states = 0
    
    while len(frontier) > 0:
        state = frontier.pop(0)
        (timeLeft, aGoal, bGoal, aTime, bTime, openV, pastFlow) = state
        # print(state)

        # if 26 - timeLeft + 1 == 11:
        #     print(state)

        if (timeLeft, aGoal, bGoal, aTime, bTime, frozenset(openV), pastFlow) in visited_states: continue
        visited_states.add((timeLeft, aGoal, bGoal, aTime, bTime, frozenset(openV), pastFlow))
        # visited_states.add((timeLeft, bGoal, aGoal, bTime, aTime, frozenset(openV), pastFlow))

        num_states += 1

        currFlow = sum([flow[x] for x in openV])

        nextCaves = [x for x in flow if x not in openV]
        if aTime > 0 and aGoal in nextCaves: nextCaves.remove(aGoal)
        if bTime > 0 and bGoal in nextCaves: nextCaves.remove(bGoal)

        if timeLeft == 0 or (len(nextCaves) == 0 and aTime + bTime == 0):
            finalFlow = pastFlow + currFlow * timeLeft
            if finalFlow >= maxFinalFlow: final_state = (timeLeft, aGoal, bGoal, aTime, bTime, frozenset(openV), pastFlow) 
            maxFinalFlow = max(maxFinalFlow, finalFlow)
            # print(state)
            # print('finished')

        
        perms = set(permutations(nextCaves, 2))

        if len(nextCaves) == 1:
            # print('caught')
            aGoalNext, bGoalNext = (nextCaves[0], bGoal) if aTime == 0 else (aGoal, nextCaves[0])

            # aTimeNext = dists[(aGoal, aGoalNext)] + 1 if aTime == 0 else aTime
            # bTimeNext = dists[(bGoal, bGoalNext)] + 1 if bTime == 0 else bTime

            aTimeNext, bTimeNext = (dists[(aGoal, aGoalNext)] + 1, bTime) if aTime == 0 else (aTime, dists[(bGoal, bGoalNext)] + 1)

            timeToPass = min(aTimeNext, bTimeNext, timeLeft)
            timeLeftNext = timeLeft - timeToPass

            aTimeNext = max(aTimeNext - timeToPass, 0)
            bTimeNext = max(bTimeNext - timeToPass, 0)

            flowNext = pastFlow + currFlow * timeToPass

            openVNext = openV.copy()
            if aTimeNext == 0: openVNext = openVNext.union([aGoalNext])
            if bTimeNext == 0: openVNext = openVNext.union([bGoalNext])
 
            come_from[(timeLeftNext, aGoalNext, bGoalNext, aTimeNext, bTimeNext, frozenset(openVNext), flowNext)] = (timeLeft, aGoal, bGoal, aTime, bTime, frozenset(openV), pastFlow)
            stateNext = (timeLeftNext, aGoalNext, bGoalNext, aTimeNext, bTimeNext, openVNext, flowNext)
            # print('adding state:', stateNext)
            frontier.append(stateNext)

        for (goal1, goal2) in perms:
            aGoalNext = goal1 if aTime == 0 else aGoal
            bGoalNext = goal2 if bTime == 0 else bGoal

            # if aGoalNext == bGoalNext: continue

            aTimeNext = dists[(aGoal, aGoalNext)] + 1 if aTime == 0 else aTime
            bTimeNext = dists[(bGoal, bGoalNext)] + 1 if bTime == 0 else bTime

            timeToPass = min(aTimeNext, bTimeNext, timeLeft)
            timeLeftNext = timeLeft - timeToPass

            aTimeNext = max(aTimeNext - timeToPass, 0)
            bTimeNext = max(bTimeNext - timeToPass, 0)

            flowNext = pastFlow + currFlow * timeToPass

            openVNext = openV.copy()
            if aTimeNext == 0: openVNext = openVNext.union([aGoalNext])
            if bTimeNext == 0: openVNext = openVNext.union([bGoalNext])
 
            come_from[(timeLeftNext, aGoalNext, bGoalNext, aTimeNext, bTimeNext, frozenset(openVNext), flowNext)] = (timeLeft, aGoal, bGoal, aTime, bTime, frozenset(openV), pastFlow)
            stateNext = (timeLeftNext, aGoalNext, bGoalNext, aTimeNext, bTimeNext, openVNext, flowNext)
            # print('adding state:', stateNext)
            frontier.append(stateNext)
    print(maxFinalFlow)
    
    while final_state != None:
        print(final_state)
        final_state = come_from[final_state]

    return maxFinalFlow


if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day16_part1(example_input) == 1651
    print(day16_part1(test_input))

    # assert day16_part2(example_input) == 1707
    # print(day16_part2(test_input))