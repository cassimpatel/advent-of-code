from functools import cmp_to_key

# returns True if a definitive smaller item in the left packet is found or end of L is reached
# returns False if a definitive larger item in the left packet is found or end of R is reached
# returns None if no definitive item is found and the packets have same length
def rightOrder(lPacket, rPacket, indent = 0):
    lType, rType = type(lPacket), type(rPacket)

    if lType == rType == type(1):
        return None if lPacket == rPacket else lPacket < rPacket

    lPacket = [lPacket] if type(lPacket) is int else lPacket
    rPacket = [rPacket] if type(rPacket) is int else rPacket

    # print(''.join(['\t']*indent), end='')
    # print('- compare', lPacket, 'vs', rPacket)

    i = 0
    while i < len(lPacket):
        if i >= len(rPacket): return False
        subResult = rightOrder(lPacket[i], rPacket[i], indent+1)
        if subResult != None: return subResult
        i += 1
        
    # if broke out because lPacket is shorter, return True, otherwise None
    return None if len(lPacket) == len(rPacket) else True


def day13_part1(input):
    packetPairs = [[eval(y) for y in x.split('\n')] for x in input.split('\n\n')]
    result = 0

    for i in range(len(packetPairs)):
        packetIndex = i + 1
        [lPacket, rPacket] = packetPairs[i]
        if rightOrder(lPacket, rPacket) == True:
            result += packetIndex

    return result

def day13_part2(input):
    # comparison function for which packet comes first
    def comparison_func(L, R):
        return -1 if rightOrder(L, R) == True else 1

    packets= [eval(x) for x in input.split('\n') if x != '']
    packets += [[[2]], [[6]]]
    
    packets = sorted(packets, key=cmp_to_key(comparison_func))
    divider1, divider2 = packets.index([[2]]) + 1, packets.index([[6]]) + 1

    return divider1 * divider2

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day13_part1(example_input) == 13
    print(day13_part1(test_input))

    assert day13_part2(example_input) == 140
    print(day13_part2(test_input))