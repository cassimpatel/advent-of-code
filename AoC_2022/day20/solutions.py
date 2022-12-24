class Node:
    def __init__(self, value, n_elem, next = None, prev = None):
        self.val = value
        self.next = next
        self.prev = prev
        self.n = n_elem

        # calculate whether moving left or right when mixing is optimal
        rMoves, lMoves = self.val % (self.n - 1), self.n - 1 - (self.val % (self.n - 1))
        self.num_moves = min(lMoves, rMoves)
        self.dir = 'L' if lMoves < rMoves else 'R'
    
    def move(self):
        # remove node from the doubly linked list, stitch together prv and nxt
        prv, nxt = self.prev, self.next
        prv.next, nxt.prev = nxt, prv

        # move number of steps required in the right direction
        for _ in range(self.num_moves):
            prv, nxt = (nxt, nxt.next) if self.dir == 'R' else (prv.prev, prv)

        # insert node back into the doubly linked list
        self.prev, self.next = prv, nxt
        prv.next, nxt.prev = self, self

# take a list of numbers, return the mixed list with 0 first
def mix_file(orig_list, num_times = 1):
    # tracking length of list and position of number 0 for traversal later
    n = len(orig_list)
    node_0 = None

    # we need a doubly linked list and a list of references (to maintain original order for mixing)
    start = currEnd = Node(orig_list[0], n)
    elements = [start]

    # build out doubly linked list and append references, tracking reference to 0 number
    for x in orig_list[1:]:
        newEnd = Node(x, n, start, currEnd)
        node_0 = newEnd if x == 0 else node_0
        currEnd.next, start.prev, currEnd = newEnd, newEnd, newEnd
        elements.append(newEnd)

    # for each round, loop over original order and apply moves
    for i in range(num_times):
        # print('iter', i)
        for x in elements:
            x.move()

    elements = []
    i = node_0
    while True:
        elements.append(i.val)
        i = i.next
        if i is node_0: break

    return elements

def day20_part1(input):
    orig_list = [int(x) for x in input.split('\n')]
    new_list = mix_file(orig_list)
    n = len(new_list)
    
    a, b, c = new_list[1000 % n], new_list[2000 % n], new_list[3000 % n]
    return a + b + c

def day20_part2(input):
    orig_list = [int(x) * 811589153 for x in input.split('\n')]
    new_list = mix_file(orig_list, 10)
    n = len(new_list)
    
    a, b, c = new_list[1000 % n], new_list[2000 % n], new_list[3000 % n]
    return a + b + c

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day20_part1(example_input) == 3
    print(day20_part1(test_input))

    assert day20_part2(example_input) == 1623178306
    print(day20_part2(test_input))