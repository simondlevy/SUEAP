#!/usr/bin/env python3
'''
Use NSGS-II to solve multiobjective fitness problem from Fonseca and Fleming (1993)

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

from sueap import Problem
from sueap.nsga2 import NSGA2

class Fon(Problem):

    PM   = .01
    PC   = .7

    def new_params(self):
        return 8 * np.random.random(3) - 4

    @staticmethod
    def eval(p):
        return np.array((1 - np.exp(-np.sum((p.x-1/np.sqrt(3))**2)), (1 - np.exp(-np.sum((p.x+1/np.sqrt(3))**2)))))

    @staticmethod
    def mutate(p, g, G):
        p.x += np.random.randn(3) * Fon.PM * (G-g)/G

    @property
    def fmin(self):
        return 0,0

    @property
    def fmax(self):
        return 1,1

    @property
    def fsiz(self):
        return 2

    @property
    def pc(self):
        return self.PC

    @staticmethod
    def crossover(p, q):

        k = np.random.randint(3-1) + 1
        return np.append(p.x[:k], q.x[k:])

if __name__ == '__main__':

    np.random.seed(0)

    nsga2 = NSGA2(Fon(), 8)
    nsga2.run(1)
