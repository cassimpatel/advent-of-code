import re
from math import floor

def prep_input(input):
    input = [x.split('\n') for x in input.split('\n\n')]
    monkeys = {x:{} for x in range(len(input))}

    for [monkeyName, startItems, operation, test, testTrue, testFalse] in input:
        monkeyId = int(re.findall(r'\d+', monkeyName)[0])
        monkeys[monkeyId]['items'] = [int(x) for x in re.findall(r'\d+', startItems)]
        monkeys[monkeyId]['operation'] = operation.replace('  Operation: new = ', '')
        monkeys[monkeyId]['divisibleTest'] = int(test.split()[-1])
        monkeys[monkeyId][True] = int(testTrue.split()[-1])
        monkeys[monkeyId][False] = int(testFalse.split()[-1])

    return monkeys

def day11_part1(input):
    monkeys = prep_input(input)
    numMonkeys = len(monkeys.keys())
    numInspections = {x:0 for x in range(numMonkeys)}

    for round in range(20):
        for monkeyID in range(numMonkeys):
            numInspections[monkeyID] += len(monkeys[monkeyID]['items'])

            while len(monkeys[monkeyID]['items']) > 0:
                old = monkeys[monkeyID]['items'].pop(0)
                new = eval(monkeys[monkeyID]['operation'])
                new = floor(new / 3)
                destMonkey = monkeys[monkeyID][new % monkeys[monkeyID]['divisibleTest'] == 0]
                monkeys[destMonkey]['items'].append(new)

    numInspections = sorted(numInspections.values())
    return numInspections[-1] * numInspections[-2]

def day11_part2(input):
    monkeys = prep_input(input)
    numMonkeys = len(monkeys.keys())
    numInspections = {x:0 for x in range(numMonkeys)}

    # to prevent the numbers getting too large: we can take a common modulus
    # if we take the product of all monkeys divTest, doing this mod should not affect any monkeys calculation
    # since we are only taking the modulus, this should not affect the monkeys operation either
    commonDivisor = 1
    for monkeyID in range(numMonkeys):
        commonDivisor *= monkeys[monkeyID]['divisibleTest']

    for round in range(10000):
        for monkeyID in range(numMonkeys):
            numInspections[monkeyID] += len(monkeys[monkeyID]['items'])

            while len(monkeys[monkeyID]['items']) > 0:
                old = monkeys[monkeyID]['items'].pop(0)
                new = eval(monkeys[monkeyID]['operation'])

                # rather than /3 we do this to keep numbers smaller
                new %= commonDivisor

                destMonkey = monkeys[monkeyID][new % monkeys[monkeyID]['divisibleTest'] == 0]
                monkeys[destMonkey]['items'].append(new)

    numInspections = sorted(numInspections.values())
    return numInspections[-1] * numInspections[-2]

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day11_part1(example_input) == 10605
    print(day11_part1(test_input))

    assert day11_part2(example_input) == 2713310158
    print(day11_part2(test_input))