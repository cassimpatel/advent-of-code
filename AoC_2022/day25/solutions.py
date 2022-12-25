def day25_part1(input):
    val = {
        '2': 2, '1': 1, '0': 0, '-': -1, '=': -2,
        2: '2', 1: '1', 0: '0', -1: '-', -2: '='
    }
    
    input = input.split('\n')
    # value in each place where 1 is the last place
    result = {1: 0}

    # working from right to left, calculate value and carry over
    i = 1
    while True:
        places = [x[-i] for x in input if len(x) >= i]
        placesSum = sum([val[x] for x in places]) + result[i]
        if len(places) == 0: break

        result[i] = ((placesSum + 2) % 5) - 2
        result[i+1] = (placesSum + 2) // 5
        i += 1

    # continue calculating carry over until they are resolved
    i = max(result.keys())
    while True:
        if result[i] in [2, 1, 0, -1, -2]: break
        result[i] = ((result[i] + 2) % 5) - 2
        result[i+1] = (result[i] + 2) // 5
        i += 1

    str_result = "".join([val[result[x]] for x in range(max(result.keys())-1, 0, -1)])
    return str_result

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day25_part1(example_input) == '2=-1=0'
    print(day25_part1(test_input))