import re
from collections import defaultdict

def getSensorData(input):
    sensors = [[int(y) for y in re.findall(r'[-]?\d+', x)] for x in input.split('\n')]
    for i, [sx, sy, bx, by] in enumerate(sensors):
        manhattanDist = abs(sx-bx) + abs(sy-by)
        sensors[i].append(manhattanDist)
    return sensors

def day15_part1(input, y):
    sensors = getSensorData(input)

    covered = set([])
    for [sx, sy, bx, by, d] in sensors:
        # print(sx, sy, bx, by, d)

        # the y row is not in range of the sensor
        if abs(y - sy) > d: continue
        
        # otherwise calc potential x range in y row
        dx = d - abs(y - sy)
        x1, x2 = dx + sx, -dx + sx
        xlocs = range(min(x1, x2), max(x1, x2)+1)
        
        covered.update(xlocs)
        if y == by:
            # the beacon took up a loc in y: remove bx
            covered.discard(bx)

    return len(covered)

# generate set of points with manhattan distance d away from (x, y)
def generatePoints(x, y, d):
    points = set([])
    for dx in range(-d, d+1):
        dy = [-(d - abs(dx)), d - abs(dx)]
        newPoints = [(x+dx, y+dy[0]), (x+dx, y+dy[1])]
        points.update(newPoints)
    return points

def day15_part2(input, maxXY):
    sensors = getSensorData(input)

    for [sx, sy, bx, by, d] in sensors:
        # print(sx, sy, bx, by, d)

        # Since there is only one distress signal location, we can restrict the search space to locations just outside each signal diamond
        for (x, y) in generatePoints(sx, sy, d+1):
            if x < 0 or x > maxXY: continue
            if y < 0 or y > maxXY: continue

            # Check if the location sits in the field for any signal
            found = True
            for [sx1, sy1, bx1, by1, d1] in sensors:
                if abs(sx1 - x) + abs(sy1 - y) <= d1:
                    found = False
                    break
            if found:
                # print(x, y)
                return (4000000 * x) + y
            
    return 'LOCATION NOT FOUND'

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day15_part1(example_input, 10) == 26
    print(day15_part1(test_input, 2000000))

    assert day15_part2(example_input, 20) == 56000011
    print(day15_part2(test_input, 4000000))