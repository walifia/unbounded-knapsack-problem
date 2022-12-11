from matplotlib import pyplot as plt
import numpy as np
import sys

args = sys.argv
t_first = int(args[1])
T = int(args[2])

for t in range(t_first, t_first + T):
    plt.clf()
    plt.grid()
    with open('testsuite/' + str(t) + '.conv', "r", encoding = "utf-8") as f:
        data = []
        for line in f:
            values = [int(c) for c in (line.split(sep = ','))]
            indices = [i + 1 for i in range(len(values))]
            plt.plot(indices, values, color = 'green')
            data.append(values)
        data_T = np.matrix(data).T
        data_T = data_T.tolist()
        indices = [i + 1 for i in range(len(data_T))]
        ci_lbnd = int(.05 * len(data_T[0]))
        ci_upbnd = int(.95 * len(data_T[0]))
        ci_l = []
        ci_up = []
        avg = []
        for it in data_T:
            it.sort()
            ci_l.append(it[ci_lbnd])
            ci_up.append(it[ci_upbnd])
            avg.append(sum(it) // len(it))
        plt.plot(indices, ci_l, color = 'red')
        plt.plot(indices, ci_up, color = 'red')
        plt.plot(indices, avg, color = 'blue')
    plt.savefig('convergence_graphs/' + str(t) + '.pdf')
            
