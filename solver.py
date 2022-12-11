import sys

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def knapsack(items, capacity):
    n = len(items)
    table = [[0] * (capacity + 1) for i in range(n)]

    for i in range(n):
        table[i][0] = 0

    for c in range(capacity + 1):
        table[0][c] = (c // items[0].weight) * items[0].value

    for i in range(1, n):
        for c in range(1, capacity + 1):
            if (items[i].weight <= c):
                table[i][c] = max(table[i - 1][c], items[i].value + table[i][c - items[i].weight])
            else:
                table[i][c] = table[i - 1][c]

    return table[i][c], pick_selected_items(table, items)


def pick_selected_items(table, items):
    i, c = len(table) - 1, len(table[0]) - 1
    total_profit = table[i][c]

    solution = [0 for i in range(len(items))]

    while (i - 1 >= 0 and table[i][c] >= 0):
        if (table[i][c] != table[i - 1][c]):
            solution[i] += 1
            c -= items[i].weight
            total_profit -= items[i].value
        else:
            i -= 1

    while (total_profit > 0):
        solution[0] += 1
        total_profit -= items[0].value
    
    return solution


def get_test(t):
    filename = str(t)
    f = open('testsuite/' + filename + '.test', "r", encoding = "utf-8")
    n, W = map(int, (f.readline().split()))
    w = [int(c) for c in (f.readline().split(sep = ','))]
    p = [int(c) for c in (f.readline().split(sep = ','))]
    items = [Item(w[i], p[i]) for i in range(n)]
    f.close()
    return (n, W, items)

def solve(t_start, T):
    for t in range(t_start, t_start + T):
        n, W, items = get_test(t)
        f = open('testsuite/' + str(t) + '.ans', "w", encoding = "utf-8")
        profit, ans_set = knapsack(items, W)
        f.write(str(profit) + '\n' + str(ans_set)[1:-1:])
        f.close()

args = sys.argv
t_first = int(args[1])
T = int(args[2])
solve(t_first, T)