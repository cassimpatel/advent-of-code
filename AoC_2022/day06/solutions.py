def day6_part1(input):
    for i in range(3, len(input)+1):
        substr = input[i-4:i]
        if len(set(substr)) == 4:
            return i
    return 'NO START OF PACKET FOUND'

def day6_part2(input):
    for i in range(13, len(input)+1):
        substr = input[i-14:i]
        if len(set(substr)) == 14:
            return i
    return 'NO START OF PACKET FOUND'

if __name__ == "__main__":
    
    example_1 = 'mjqjpqmgbljsphdztnvjfqwrcgsmlb'
    example_2 = 'bvwbjplbgvbhsrlpgdmjqwftvncz'
    example_3 = 'nppdvjthqldpwncqszvftbrmjlhg'
    example_4 = 'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'
    example_5 = 'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
    test_input = open('input.txt', 'r').read()

    assert day6_part1(example_1) == 7
    assert day6_part1(example_2) == 5
    assert day6_part1(example_3) == 6
    assert day6_part1(example_4) == 10
    assert day6_part1(example_5) == 11
    print(day6_part1(test_input))

    assert day6_part2(example_1) == 19
    assert day6_part2(example_2) == 23
    assert day6_part2(example_3) == 23
    assert day6_part2(example_4) == 29
    assert day6_part2(example_5) == 26
    print(day6_part2(test_input))