def day17_part1(input):
    # 1 means right and 0 means left
    jets = [-1 if x == '<' else 1 for x in input]
    tower = [0] * 7

    # rocks data encoded as heights of the bottom of the boulder then heights of the top of the boulder
    # this moves across the 4 width to account for the widest 
    rocks = [

    ]

    return None

def day17_part2(input):
    return None

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day17_part1(example_input) == 13068
    print(day17_part1(test_input))

    # assert day17_part2(example_input) == 56000011
    # print(day17_part2(test_input)