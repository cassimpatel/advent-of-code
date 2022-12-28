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

# produces a state tuple given time remaining value and a resources dictionary
def generate_state(timeRem, resources):
    return (timeRem, resources['ore'], resources['oreR'], resources['cla'], resources['claR'], resources['obs'], resources['obsR'], resources['geo'], resources['geoR'])

# returns the sum of integers m, ..., n - 1 (equal to sum(range(m, n)))
def seq_sum(m, n):
    n -= 1
    return int(0.5 * (n + m) * (n - m + 1))

# find the maximal geodes that can be mined using blueprint in search_time via DFS
def get_max_geodes(blueprint, search_time):
    # calculate the maximum of each resource needed for any robot creation (for pruning)
    max_required = {'ore': 0, 'cla': 0, 'obs': 0}
    for rob in blueprint:
        for res in blueprint[rob]:
            max_required[res] = max(max_required[res],  blueprint[rob][res])

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
            # no more time left: calculate geode output and compare to max
            max_geodes = max(max_geodes, geo + geoR)
            continue
        elif oreR >= blueprint['geoR']['ore'] and obsR >= blueprint['geoR']['obs']:
            # we produce enough ore and obs to make a geoR every remaining turn: calc potential geo output and prune
            potential_geo = geo + seq_sum(geoR, geoR + timeRem)
            max_geodes = max(max_geodes, potential_geo)
            continue
        elif geo + seq_sum(geoR, geoR + timeRem) < max_geodes:
            # even creating a geoR every turn we can't beat the current max: prune this state
            continue
        elif oreR > max_required['ore'] or claR > max_required['cla'] or obsR > max_required['obs']:
            # we are unnecessarily creating more robots than required: prune this state
            continue

        # calculate robots that can be produced given current resources
        potential_robots = [rob for rob in blueprint if False not in [resources[y] >= blueprint[rob][y] for y in blueprint[rob]]]
        # if we can make a geoR, this is the optimal move: don't consider other options
        if 'geoR' in potential_robots: potential_robots = ['geoR']

        # update resource counts according to number of robots
        resources = {x: resources[x] + resources[x + 'R'] if x in ['ore', 'cla', 'obs', 'geo'] else resources[x] for x in resources}

        # there are no robot that can be made: new state is just waiting and doing nothing
        if len(potential_robots) == 0:
            next_state = generate_state(timeRem-1, resources)
            if next_state in come_from_state: continue
            come_from_state[next_state] = curr_state
            frontier.insert(0, next_state)
            continue

        # for each robot, make a new resources copy, deduct relevant resources, append new state
        for potential_rob in potential_robots:
            next_resources = resources.copy()
            next_resources[potential_rob] += 1
            for res in blueprint[potential_rob]:
                next_resources[res] -= blueprint[potential_rob][res]
            next_state = generate_state(timeRem-1, next_resources)
            if next_state in come_from_state: continue
            frontier.insert(0, next_state)
            come_from_state[next_state] = curr_state
        
        # if there is a robot that could be created in the future using more ore than we have now (we can't create it this turn) then add waiting as a possibility
        max_next_ore_required = max([blueprint[rob]['ore'] for rob in potential_robots])
        if max_next_ore_required == max_required['ore']: continue
        next_state = generate_state(timeRem-1, resources)
        if next_state in come_from_state: continue
        frontier.insert(0, next_state)
        come_from_state[next_state] = curr_state

    return max_geodes
    
def day19_part1(input):
    blueprints = parse_input(input)
    result = 0

    for i, blueprint in enumerate(blueprints):
        max_geodes = get_max_geodes(blueprint, 24)
        # print('blueprint {}: max geodes {}'.format(i+1, max_geodes))
        result += (i + 1) * max_geodes

    return result

def day19_part2(input):
    blueprints = parse_input(input)[:3]
    result = 1

    for i, blueprint in enumerate(blueprints):
        max_geodes = get_max_geodes(blueprint, 32)
        # print('blueprint {}: max geodes {}'.format(i+1, max_geodes))
        result *= max_geodes

    return result

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day19_part1(example_input) == 33
    print(day19_part1(test_input))

    assert day19_part2(example_input) == 3472
    print(day19_part2(test_input))