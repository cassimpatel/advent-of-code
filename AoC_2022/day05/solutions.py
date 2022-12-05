import re

def prep_input(input):
    [start_config, moves] = input.split('\n\n')

    # split moves list by lines, extract integers as (num_boxes, src, dest) combinations
    moves = [[int(y) for y in re.findall(r'\b\d+\b', x)] for x in moves.split('\n')]
    
    # extract ints from last line of configuration and setup empty dictionary of stacks
    stacks = {int(x):[] for x in start_config.split('\n')[-1].split('   ')}

    # remove indices at bottom
    start_config = start_config.split('\n')[:-1]
    
    # for each of the stacks, we get the index in the strings where that stacks char is
    for stack_index in stacks:
        char_index = 4 * stack_index - 3

        # working through the bottom of the stack first: find the char and push to the stack
        for stack_level in start_config[::-1]:
            if stack_level[char_index] == ' ': break
            stacks[stack_index].append(stack_level[char_index])

    return (stacks, moves)

def day5_part1(input):
    stacks, moves = prep_input(input)

    for [num_boxes, src_stack, dest_stack] in moves:
        # print(num_boxes, src_stack, dest_stack)
        for _ in range(num_boxes):
            stacks[dest_stack].append(stacks[src_stack].pop())
        # print(stacks)

    # join last element in each stack to get result
    return ''.join([stacks[x][-1] for x in stacks])

def day5_part2(input):
    stacks, moves = prep_input(input)

    for [num_boxes, src_stack, dest_stack] in moves:
        # print(num_boxes, src_stack, dest_stack)

        # get the list of boxes to move, remove from src stack, append to dest stack
        moved_boxes = stacks[src_stack][-num_boxes:]
        stacks[src_stack] = stacks[src_stack][:-num_boxes]
        stacks[dest_stack] += moved_boxes
        # print(stacks)

    # join last element in each stack to get result
    return ''.join([stacks[x][-1] for x in stacks])

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day5_part1(example_input) == 'CMZ'
    print(day5_part1(test_input))

    assert day5_part2(example_input) == 'MCD'
    print(day5_part2(test_input))