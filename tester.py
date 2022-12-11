import sys
import os

args = sys.argv

os.system("python3 b_n_b.py " + " ".join(args[1:3]))
os.system("python3 solver.py " + " ".join(args[1:3]))

args = sys.argv
t_start = int(args[1])
T = int(args[2])

for t in range(t_start, t_start + T):
    fn1 = "testsuite/" + str(t) + ".bnb"
    fn2 = "testsuite/" + str(t) + ".ans"
    with open(fn1, "r", encoding = "utf-8") as f:
        data1 = f.readline()
    with open(fn2, "r", encoding = "utf-8") as f:
        data2 = f.readline()
    if (data1 != data2):
        print(t)

""" for t in range(t_start, t_start + T):
    for k in range(100):
        os.system("python3 pso.py " + " ".join([str(t), '1']) + " " + " ".join(args[3:5])) """


