def parse_input(input):
    input = input.replace('\n  ', ' ').replace('\n\n', '\n').split('\n')
    blueprints = []

    # forming a list of blueprints: where each is a dictionary of dictionaries
    for x in input:
        pts = x.split()
        oreRore, claRore, obsRore, obsRcla, geoRore, geoRobs = int(pts[6]), int(pts[12]), int(pts[18]), int(pts[21]), int(pts[27]), int(pts[30])
        blueprint = {'oreR': {'ore': oreRore}, 'claR': {'ore': claRore}, 'obsR': {'ore': obsRore, 'cla': obsRcla}, 'geoR': {'ore': geoRore, 'obs': geoRobs}}
        blueprints.append(blueprint)

    return blueprints
    
def get_max_geodes(blueprint, search_time):
    # we can calculate the maximum of each resource needed for any robot creation
    # then, we shouldn't ever create more robots than the max for their type (limiting search space)
    max_required = {'ore': 0, 'cla': 0, 'obs': 0}
    for rob in blueprint:
        for res in blueprint[rob]:
            max_required[res] = max(max_required[res],  blueprint[rob][res])

    ore_required = {rob: blueprint[rob]['ore'] for rob in blueprint}

    # represent states as (timeRemaining, ore, oreR, cla, claR, obs, obsR, geo, geoR)
    start_state = (search_time, 0, 1, 0, 0, 0, 0, 0, 0)
    frontier = [start_state]
    come_from_state = {start_state: None}
    max_geodes = 0

    while len(frontier) > 0:
        (timeRem, ore, oreR, cla, claR, obs, obsR, geo, geoR) = curr_state =  frontier.pop(0)
        resources = {'ore': ore, 'oreR': oreR, 'cla': cla, 'claR': claR, 'obs': obs, 'obsR': obsR, 'geo': geo, 'geoR': geoR}
        # print(curr_state)
        
        if timeRem == 1:
            # no more time left
            # print(curr_state)
            # print(geo)
            # print('reached a final state')
            max_geodes = max(max_geodes, geo + geoR)
            continue
        elif geo + sum(range(geoR, geoR + timeRem)) < max_geodes:
            # print('pruned due to not meeting current best')
            # even creating a geoR every turn we can't beat the current max: prune this state
            continue
        elif oreR >= blueprint['geoR']['ore'] and obsR >= blueprint['geoR']['obs']:
            # we have enough to make a geoR every remaining turn: calc potential geo output and prune
            potential_geo = geo + sum(range(geoR, geoR + timeRem))
            max_geodes = max(max_geodes, potential_geo)
            # print('calculated potential best score due to meeting geoR spec')
            continue
        elif oreR > max_required['ore'] or claR > max_required['cla'] or obsR > max_required['obs']:
            # unnecessarily creating extra robots than required: prune this state
            # print('pruned due to creating more tahn needed')
            continue

        # generate neighbours: for each, set come_from_state
        potential_robots = [rob for rob in blueprint if False not in [resources[y] >= blueprint[rob][y] for y in blueprint[rob]]][::-1]

        # update resource counts
        resources = {x: resources[x] + resources[x + 'R'] if x in ['ore', 'cla', 'obs', 'geo'] else resources[x] for x in resources}

        if len(potential_robots) == 0:
            next_state = (timeRem - 1, resources['ore'], resources['oreR'], resources['cla'], resources['claR'], resources['obs'], resources['obsR'], resources['geo'], resources['geoR'])
            frontier.insert(0, next_state)
            come_from_state[next_state] = curr_state

        if 'geoR' in potential_robots:
            next_resources = resources.copy()
            next_resources['geoR'] += 1
            for res in blueprint['geoR']:
                next_resources[res] -= blueprint['geoR'][res]
            next_state = (timeRem - 1, next_resources['ore'], next_resources['oreR'], next_resources['cla'], next_resources['claR'], next_resources['obs'], next_resources['obsR'], next_resources['geo'], next_resources['geoR'])
            if next_state in come_from_state: continue
            frontier.insert(0, next_state)
            come_from_state[next_state] = curr_state
            continue


        # append neighbours
        for potential_rob in potential_robots:
            next_resources = resources.copy()
            next_resources[potential_rob] += 1
            for res in blueprint[potential_rob]:
                next_resources[res] -= blueprint[potential_rob][res]
            next_state = (timeRem - 1, next_resources['ore'], next_resources['oreR'], next_resources['cla'], next_resources['claR'], next_resources['obs'], next_resources['obsR'], next_resources['geo'], next_resources['geoR'])
            if next_state in come_from_state: continue
            frontier.insert(0, next_state)
            come_from_state[next_state] = curr_state
        
        for potential_rob in potential_robots:
            if ore_required[potential_rob] <= max(ore_required.values()):
                next_state = (timeRem - 1, resources['ore'], resources['oreR'], resources['cla'], resources['claR'], resources['obs'], resources['obsR'], resources['geo'], resources['geoR'])
                frontier.insert(0, next_state)
                come_from_state[next_state] = curr_state
            break
    print(max_geodes)
    return max_geodes
    
def day19_part1(input):
    # separate out a function to calculate the score for a single blueprint so we can iterate over blueprints easily
    # this function will do a simple DFS to maximise the score, with agressive pruning where possible
    # we should never have more robots of any given type than the maximum required of that resource for any robot creation (as we can only make one robot a round and resources replenish)
    # if we can make a geode robot that is the optimal move: we shouldn't explore other options
    # taking the current best score, if we can't do better than it in the remaining time (assume making a geode robot every remaining turn) that node has no potential, pune it
    # make sure to keep a dict of where nodes have been visited from so you can backtrack from the optimal solution
    # if you can make a robot, only consider waiting if waiting means you could build a different robot in the future (b has cost strictly more than a)
    
    blueprints = parse_input(input)
    result = 0

    for i, blueprint in enumerate(blueprints):
        quality_level = (i + 1) * get_max_geodes(blueprint, 24)
        print('blueprint {}: quality_level {}'.format(i+1, quality_level))
        result += quality_level
        # break

    return result

def day19_part2(input):
    blueprints = parse_input(input)[:3]
    result = 1

    for i, blueprint in enumerate(blueprints):
        print('blueprint', i + 1)
        quality_level = get_max_geodes(blueprint, 32)
        print('quality_level', quality_level)
        result *= quality_level
        # break

    return result

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    # assert day19_part1(example_input) == 33
    # print(day19_part1(test_input))

    assert day19_part2(example_input) == 3472
    print(day19_part2(test_input))