def day19_part1(input):
    # separate out a function to calculate the score for a single blueprint so we can iterate over blueprints easily
    # this function will do a simple DFS to maximise the score, with agressive pruning where possible
    # we should never have more robots of any given type than the maximum required of that resource for any robot creation (as we can only make one robot a round and resources replenish)
    # if we can make a geode robot that is the optimal move: we shouldn't explore other options
    # taking the current best score, if we can't do better than it in the remaining time (assume making a geode robot every remaining turn) that node has no potential, pune it
    # make sure to keep a dict of where nodes have been visited from so you can backtrack from the optimal solution
    # if you can make a robot, only consider waiting if waiting means you could build a different robot in the future (b has cost strictly more than a)
    # represent states as (timeRemaining, ore, oreR, cla, claR, obs, obsR, geo, geoR)
    return None

def day19_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day19_part1(example_input) == 33
    print(day19_part1(test_input))

    # assert day19_part2(example_input) == 1
    # print(day19_part2(test_input))