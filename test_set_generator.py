from numpy.random import default_rng
import sys

class Test():
    def __init__(self):
        self.n = 0
        self.w = []
        self.p = []
        self.W = 0

    def generate(self, n_min, n_max, w_min, w_max, p_min, p_max):
        rng = default_rng()
        self.n = rng.integers(low = n_min, high = n_max + 1)
        self.w = randlist(self.n, w_min, w_max)
        self.p = randlist(self.n, p_min, p_max)
        self.W = sum(self.w) // 2

    def fprintf(self, test_n):
        f = open("testsuite/{}.test".format(test_n + 1), "w", encoding = "utf-8")
        f.write(str(self.n) + ' ' + str(self.W) + '\n')
        f.write(str(self.w)[1:-1:] + '\n')
        f.write(str(self.p)[1:-1:])
        f.close()

def randlist(n, low, high):
    rng = default_rng()
    res = []
    res_v = set()
    while (len(res) < n):
        new_v = rng.integers(low = low, high = high + 1)
        if (not (new_v in res_v)):
            res.append(new_v)
            res_v.add(new_v)
    return res



args = sys.argv
             
T = int(args[1])
n_min = int(args[2])
n_max = int(args[3])
w_min = int(args[4])
w_max = int(args[5])
p_min = int(args[6])
p_max = int(args[7])

for t in range(T): 
    _T = Test()
    _T.generate(n_min, n_max, w_min, w_max, p_min, p_max)
    _T.fprintf(t)