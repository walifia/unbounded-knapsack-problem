import numpy as np
import math
import matplotlib.pyplot as plt
import sys

class Item:
    def __init__(self, weight, value):
        self.weight = weight
        self.value = value

def init_x(n, d, items, w_max):
    population = []
    rng = np.random.default_rng()
    for i in range(n):
        gene = []
        for j in range(d):
            a = rng.integers(low = 0, high = w_max // items[j].weight + 1)
            gene.append(a)
        population.append(gene)
    return population

def init_v(n, d, v_max, v_min):
    v = []
    for i in range(n):
        vi = []
        for j in range (d):
            rng = np.random.default_rng()
            a = rng.random() * (v_max - v_min) + v_min
            vi.append(a)
        v.append(vi)
    return v

def fitness(p, n, d, items, w_max):
    fitvalue = []
    fitweight = []
    for i in range(n):
        a = 0
        b = 0
        for j in range(d):
            a += items[j].weight * p[i][j]
            b += items[j].value * p[i][j]
        if (a > w_max):
            b = 0
        fitvalue.append(b)
        fitweight.append(a)
    return fitvalue

def update_p_best(p, fitvalue, p_best, px, m):
    pb = p_best
    for i in range(m):
        if fitvalue[i] > p_best[i]:
            p_best[i] = fitvalue[i]
            px[i] = p[i]
    return pb, px

def update_g_best(p, p_best, g_best, g, m):
    gb = g_best
    for i in range(m):
        if (p_best[i] > gb):
            gb = p_best[i]
            g = p[i].copy()
    return gb, g

def update_v(v, x, m, n, p_best, g, c1, c2, vmax, vmin):
    rng = np.random.default_rng()
    for i in range(m):
        a = rng.random()
        b = rng.random()
        for j in range(n):
            v[i][j] = v[i][j] + c1 * a * (p_best[i][j] - x[i][j]) + c2 * b * (g[j] - x[i][j])
            if (v[i][j] < vmin):
                v[i][j] = vmin
            if (v[i][j] > vmax):
                v[i][j] = vmax
    return v

def update_x(x, v, m, n, items, w_max):
    for i in range(m):
        for j in range(n):
            upbnd = (w_max // items[j].weight)
            x[i][j] += round(v[i][j])
            x[i][j] = max(0, x[i][j])
            x[i][j] = min(x[i][j], upbnd)
    return x

def pso_knapsack(n, W, items, population, iterations):
    #internal constant values
    c1 = 4
    c2 = 4
    v_max = 5
    v_min = -5

    g_best_conv = []

    x = init_x(population, n, items, W)
    v = init_v(population, n, v_max, v_min)
    fitness_v = fitness(x, population, n, items, W)
    p_best, p_x = fitness_v, x
    g_best, g_best_set = update_g_best(x, p_best, 0, [0 for i in range(n)], population)
    g_best_conv.append(g_best)

    v = update_v(v, x, population, n, p_x, g_best_set, c1, c2, v_max, v_min)
    x = update_x(x, v, population, n, items, W)

    for i in range(iterations):
        fitness_v = fitness(x, population, n, items, W)
        p_best, p_x = update_p_best(x, fitness_v, p_best, p_x, population)
        g_best, g_best_set = update_g_best(x, p_best, g_best, g_best_set, population)
        g_best_conv.append(g_best)
        v = update_v(v, x, population, n, p_x, g_best_set, c1, c2, v_max, v_min)
        x = update_x(x, v, population, n, items, W)
    
    return g_best, g_best_set, g_best_conv

def get_test(t):
    filename = str(t)
    f = open('testsuite/' + filename + '.test', "r", encoding = "utf-8")
    n, W = map(int, (f.readline().split()))
    w = [int(c) for c in (f.readline().split(sep = ','))]
    p = [int(c) for c in (f.readline().split(sep = ','))]
    items = [Item(w[i], p[i]) for i in range(n)]
    f.close()
    return (n, W, items)

def solve(t_start, T, population, iterations):
    for t in range(t_start, t_start + T):
        n, W, items = get_test(t)
        f = open('testsuite/' + str(t) + '.pso', "a", encoding = "utf-8")
        profit, ans_set, ans_conv = pso_knapsack(n, W, items, population, iterations)
        f.write(str(profit) + '\n' + str(ans_set)[1:-1:] + '\n')
        f.close()
        f = open('testsuite/' + str(t) + '.conv', "a", encoding = "utf-8")
        f.write(str(ans_conv)[1:-1:] + '\n')
        f.close()

args = sys.argv
t_first = int(args[1])
T = int(args[2])
population = int(args[3])
iterations = int(args[4])
solve(t_first, T, population, iterations)