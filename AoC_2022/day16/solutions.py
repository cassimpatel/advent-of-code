import re
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

def day16_part1(input):
    flow, tunnels = parseInput(input)

    # we will characterise a configuration as time left, current loc, open valves, current flow
    initialConfig = (31, 'AA', set([]), 0)
    frontier = PriorityQueue()
    frontier.put((0, initialConfig))
    # frontier = [initialConfig]

    maxFinalFlow = 0
    
    while not frontier.empty():
        (priority, (timeLeft, loc, openV, currFlow)) = frontier.get()
        print(timeLeft, loc, openV, currFlow)

        if timeLeft == 0:
            print(currFlow)
            return
            maxFinalFlow = max(currFlow, maxFinalFlow)
            continue

        nextConfigs = []

        newFlow = currFlow + sum([flow[x] for x in openV])
        priority = - newFlow
        if flow[loc] > 0 and loc not in openV:
            # nextConfigs.append((timeLeft-1, loc, openV.union([loc]), newFlow))
            frontier.put((priority-flow[loc], (timeLeft-1, loc, openV.union([loc]), newFlow)))
        for neighbour in tunnels[loc]:
            # nextConfigs.append((timeLeft-1, neighbour, openV, newFlow))
            potentialFlow = 0 if neighbour in openV else flow[neighbour]
            frontier.put((priority-potentialFlow, (timeLeft-1, neighbour, openV, newFlow)))
        
        # frontier += nextConfigs


    return maxFinalFlow

def day16_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day16_part1(example_input) == 1651
    print(day16_part1(test_input))

    # assert day16_part2(example_input) == 56000011
    # print(day16_part2(test_input)