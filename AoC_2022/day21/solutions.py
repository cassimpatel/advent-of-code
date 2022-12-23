import operator

ops = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '/' : operator.truediv,
}

def day21_part1(input):
    monkeys = {x[:4]: x.split(': ')[-1] for x in input.split('\n')}

    def getYellNum(monk):
        # print(monk)
        val = monkeys[monk]
        
        if type(val) == int:
            return val
        if len(val.split()) == 1:
            monkeys[monk] = int(val.split()[-1])
        else:
            [monk1, oper, monk2] = val.split()
            monkeys[monk] = int(ops[oper](getYellNum(monk1), getYellNum(monk2)))
        return monkeys[monk]

    return getYellNum('root')

def day21_part2(input):
    monkeys = {x[:4]: x.split(': ')[-1] for x in input.split('\n')}

    # gets the path from monk to humn if it exists
    def getHumn(monk):
        # print(monk)
        if monk == 'humn':
            return [monk]
        if len(monkeys[monk].split()) == 1: return []
        [monk1, oper, monk2] = monkeys[monk].split()
        res1, res2 = getHumn(monk1), getHumn(monk2)
        return [monk] + res1 if 'humn' in res1 else [monk] + res2

    def getYellNum(monk):
        # print(monk)
        val = monkeys[monk]

        if type(val) == int:
            return val
        if len(val.split()) == 1:
            monkeys[monk] = int(val.split()[-1])
        else:
            [monk1, oper, monk2] = val.split()
            monkeys[monk] = int(ops[oper](getYellNum(monk1), getYellNum(monk2)))
        return monkeys[monk]

    path = getHumn('root')

    # calculate the next node from root that leads to humn
    # calculate the value of that node by getting the value of the other child (since root needs both children equal)
    [rootL, op, rootR] = monkeys['root'].split()
    curr = rootL if rootL in path else rootR
    val = getYellNum(rootL) if rootR in path else getYellNum(rootR)

    # while we aren't at humn yet, find the next child to traverse to (using path)
    # find the value of the other child
    # find the supposed value of the next child using value of current node, operator and value of other child
    while curr != 'humn':
        [currL, op, currR] = monkeys[curr].split()

        next = currL if currL in path else currR
        otherVal = getYellNum(currL) if currR in path else getYellNum(currR)

        if op == '+':
            newVal = val - otherVal
        elif op == '-':
            newVal = val + otherVal if next == currL else otherVal - val
        elif op == '*':
            newVal = int(val / otherVal)
        elif op == '/':
            newVal = val * otherVal if next == currL else int(otherVal / val)

        curr, val = next, newVal

    return val

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day21_part1(example_input) == 152
    print(day21_part1(test_input))

    assert day21_part2(example_input) == 301
    print(day21_part2(test_input))