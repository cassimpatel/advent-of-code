def day10_part1(input):
    cmds = input.split('\n')
    X_register = 1
    cycleNo = 1
    result = 0
    currentCmdIndex = 0
    executingCmd = False

    while currentCmdIndex < len(cmds) or executingCmd:

        if (cycleNo + 20) % 40 == 0:
            result += cycleNo * X_register
            # print(cycleNo, X_register) 
        
        if not executingCmd:
            if cmds[currentCmdIndex] != 'noop':
                executingCmd = True
        else:
            X_register += int(cmds[currentCmdIndex].split()[1]) 
            executingCmd = False
        
        if not executingCmd: currentCmdIndex += 1
        cycleNo += 1

    return result

def day10_part2(input):
    cmds = input.split('\n')
    X_register = 1
    cycleNo = 1
    currentCmdIndex = 0
    executingCmd = False

    while currentCmdIndex < len(cmds) or executingCmd:

        spritePos = [X_register - 1, X_register, X_register + 1]
        if (cycleNo - 1) % 40 in spritePos:
            print('#', end='')
        else:
            print('.', end='')
       
        if not executingCmd:
            if cmds[currentCmdIndex] != 'noop':
                executingCmd = True
        else:
            X_register += int(cmds[currentCmdIndex].split()[1]) 
            executingCmd = False

        if not executingCmd: currentCmdIndex += 1
        cycleNo += 1

        if (cycleNo - 1) % 40 == 0: print()

    return 'Look at console for solution'

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    day10_part1(example_input) == 13140
    print(day10_part1(test_input))

    # day10_part2(example_input)
    # print()
    print(day10_part2(test_input))