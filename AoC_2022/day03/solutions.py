def getPriority(char):
    if ord(char) < 97:
        return ord(char) - 64 + 26
    return ord(char) - 96


def day3_part1(input):
    input = input.split('\n')
    string_parts = [[x[:int(len(x)/2)], x[int(len(x)/2):]] for x in input]
    result = 0
    
    for [x1, x2] in string_parts:

        x1_chars = set(x1)
        x2_chars = set(x2)
        repeated_char = list(x1_chars.intersection(x2_chars))[0]

        result += getPriority(repeated_char)

    return result

def day3_part2(input):
    input = input.split('\n')
    result = 0
    
    for i in range(0, len(input), 3):

        elf1, elf2, elf3 = input[i], input[i+1], input[i+2]
        badge_char = list(set(elf1).intersection(set(elf2)).intersection(set(elf3)))[0]
        result += getPriority(badge_char)

    return result

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day3_part1(example_input) == 157
    print(day3_part1(test_input))

    assert day3_part2(example_input) == 70
    print(day3_part2(test_input))