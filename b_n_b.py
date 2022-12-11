import queue
import sys

class Item:
    def __init__(self, pos, weight, value):
        self.pos = pos
        self.weight = weight
        self.value = value

class Node:
    def __init__(self, n, depth, weight, value):
        self.depth = depth
        self.weight = weight
        self.value = value
        self.bound = 0.
        self.set = [0 for i in range(n)]

    def __lt__(self, other):
        return self.bound < other.bound
    
def bound(u, n, W, items):
    if (u.weight >= W):
        return 0.
    
    upper_bound = u.value

    i = u.depth
    totweight = u.weight
    
    while ((i < n) and (totweight + items[i].weight <= W)):
        max_amount = (W - totweight) // items[i].weight
        totweight += max_amount * items[i].weight
        upper_bound += max_amount * items[i].value
        i += 1

    if (i < n):
        upper_bound += (W - totweight) * items[i].value / items[i].weight
    
    return upper_bound
    

def knapsack(n, W, items):
    items.sort(key = lambda x: -x.value / x.weight)

    Q = queue.PriorityQueue()
    Q.put(Node(n, -1, 0, 0))

    opt_value = 0
    opt_set = [0 for i in range(n)]

    while (not Q.empty()):
        u = Q.get()
        v1 = Node(n, -1, 0, 0)
        v2 = Node(n, -1, 0, 0)

        v1.set = u.set.copy()
        v2.set = u.set.copy()

        if (u.depth == -1):            
            v1.depth = 0
            v2.depth = 0
        else:
            v1.depth = u.depth
            v2.depth = u.depth

        v1.weight = u.weight + items[v1.depth].weight
        v1.value = u.value + items[v1.depth].value
        v1.set[v1.depth] += 1
        v1.bound = bound(v1, n, W, items) 
        if ((v1.weight <= W) and (v1.value > opt_value)):
            opt_value = v1.value
            opt_set = v1.set.copy()
        if (v1.bound > opt_value):
            Q.put(v1)

        if (u.depth != n - 1):
            v2.depth += 1
            v2.weight = u.weight
            v2.value = u.value
            v2.bound = bound(v2, n, W, items)
            if (v2.bound > opt_value):
                Q.put(v2) 

    return opt_value, opt_set


def get_test(t):
    filename = str(t)
    f = open('testsuite/' + filename + '.test', "r", encoding = "utf-8")
    n, W = map(int, (f.readline().split()))
    w = [int(c) for c in (f.readline().split(sep = ','))]
    p = [int(c) for c in (f.readline().split(sep = ','))]
    items = [Item(i, w[i], p[i]) for i in range(n)]
    f.close()
    return (n, W, items)

def solve(t_start, T):
    for t in range(t_start, t_start + T):
        n, W, items = get_test(t)
        f = open('testsuite/' + str(t) + '.bnb', "w", encoding = "utf-8")
        profit, ans_set = knapsack(n, W, items)
        ans_ordered = [0 for i in range(n)]
        for i in range(n):
            ans_ordered[items[i].pos] = ans_set[i]
        f.write(str(profit) + '\n' + str(ans_ordered)[1:-1:])
        f.close()

args = sys.argv
t_first = int(args[1])
T = int(args[2])
solve(t_first, T)