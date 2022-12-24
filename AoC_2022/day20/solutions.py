class Node:
    def __init__(self, value, n_elem, next = None, prev = None):
        self.val = value
        self.next = next
        self.prev = prev
        self.n = n_elem

        # calculate whether moving left or right when mixing is optimal
        rMoves, lMoves = self.val % (self.n-1), self.n - 1 - (self.val % (self.n-1))
        self.num_moves = min(lMoves, rMoves)
        self.dir = 'L' if lMoves < rMoves else 'R'
    
    def move(self):
        # try instead: extract the value entirely, then just move left or right n times, then insert back in
        x = self
        for _ in range(self.num_moves):
            prvprv, prv, cur, nxt, nxtnxt = x.prev.prev, x.prev, x, x.next, x.next.next
            if self.dir == 'R':
                # prv <-> cur <-> nxt <-> nxtnxt (CHANGES TO) prv <-> nxt <-> cur <-> nxtnxt
                prv.next, nxt.next, cur.next = nxt, cur, nxtnxt
                nxt.prev, cur.prev, nxtnxt.prev = prv, nxt, cur
            else:
                # prvprv <-> prv <-> cur <-> nxt (CHANGES TO) prvprv <-> cur <-> prv <-> nxt
                prvprv.next, cur.next, prv.next = cur, prv, nxt
                cur.prev, prv.prev, nxt.prev = prvprv, cur, prv

def mix_file(orig_list, num_times = 1):
    n = len(orig_list)

    # we need a doubly linked list and a list of references (to maintain original order for mixing)
    start = currEnd = Node(orig_list[0], n)
    elements = [start]

    # build out doubly linked list and append references
    for x in orig_list[1:]:
        newEnd = Node(x, n, start, currEnd)
        currEnd.next, start.prev, currEnd = newEnd, newEnd, newEnd
        elements.append(newEnd)

    # for each round, loop over original order and apply moves
    for i in range(num_times):
        # print('iter', i)
        for x in elements:
            x.move()

    elements = []
    i = start
    while True:
        elements.append(i.val)
        i = i.next
        if i is start: break

    return elements

def day20_part1(input):
    orig_list = [int(x) for x in input.split('\n')]
    n = len(orig_list)
    new_list = mix_file(orig_list)
    
    elem0 = new_list.index(0)
    a, b, c = new_list[(elem0 + 1000) % n], new_list[(elem0 + 2000) % n], new_list[(elem0 + 3000) % n]

    return a + b + c

def day20_part2(input):
    orig_list = [int(x) * 811589153 for x in input.split('\n')]
    n = len(orig_list)
    new_list = mix_file(orig_list, 10)
    
    elem0 = new_list.index(0)
    a, b, c = new_list[(elem0 + 1000) % n], new_list[(elem0 + 2000) % n], new_list[(elem0 + 3000) % n]

    return a + b + c

if __name__ == "__main__":
    example_input = open('example.txt', 'r').read()
    test_input = open('input.txt', 'r').read()

    assert day20_part1(example_input) == 3
    # print(day20_part1(test_input))

    assert day20_part2(example_input) == 1623178306
    # print(day20_part2(test_input))