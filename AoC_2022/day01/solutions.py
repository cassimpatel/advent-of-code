def day1_part1(input):
    input = [[int(y) for y in x.split('\n')] for x in input.split('\n\n')]
    return max([sum(x) for x in input])

def day1_part2(input):
    input = [[int(y) for y in x.split('\n')] for x in input.split('\n\n')]
    elf_sums = [sum(x) for x in input]
    top_three = sorted(elf_sums, reverse=True)[:3]
    return sum(top_three)

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day1_part1(example_input) == 24000
    print(day1_part1(test_input))

    assert day1_part2(example_input) == 45000
    print(day1_part2(test_input))