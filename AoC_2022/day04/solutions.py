def day4_part1(input):
    # split by pair, then per elf, then by start/end
    ranges = [[[int(z) for z in y.split('-')] for y in x.split(',')] for x in input.split('\n')]

    # number of fully contained ranges
    result = 0

    for [[elf1min, elf1max], [elf2min, elf2max]] in ranges:
        # print(elf1min, elf1max, elf2min, elf2max)

        elf1_areas = set(range(elf1min, elf1max+1))
        elf2_areas = set(range(elf2min, elf2max+1))

        if elf1_areas.issubset(elf2_areas) or elf2_areas.issubset(elf1_areas):
            result += 1

    return result

def day4_part2(input):
    # split by pair, then per elf, then by start/end
    ranges = [[[int(z) for z in y.split('-')] for y in x.split(',')] for x in input.split('\n')]

    # number of fully contained ranges
    result = 0

    for [[elf1min, elf1max], [elf2min, elf2max]] in ranges:
        # print(elf1min, elf1max, elf2min, elf2max)

        elf1_areas = set(range(elf1min, elf1max+1))
        elf2_areas = set(range(elf2min, elf2max+1))

        if len(elf1_areas & elf2_areas) > 0:
            result += 1

    return result

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day4_part1(example_input) == 2
    print(day4_part1(test_input))

    assert day4_part2(example_input) == 4
    print(day4_part2(test_input))