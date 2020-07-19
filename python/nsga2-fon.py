#!/usr/bin/env python3
import numpy as np

from sueap import Problem
from sueap.nsga2 import NSGA2

class Fon(Problem):

    PM   = .01
    PC   = .7

    def x(self):
        return 8 * np.random.random(3) - 4

    @staticmethod
    def eval(p):
        return np.array((1 - np.exp(-np.sum((p.x-1/np.sqrt(3))**2)), (1 - np.exp(-np.sum((p.x+1/np.sqrt(3))**2)))))

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

    @staticmethod
    def mutate(p, g, G):
        p.x += np.random.randn(3) * Fon.PM * (G-g)/G

if __name__ == '__main__':

    nsga2 = NSGA2(Fon(), 100)
    nsga2.animate(30)
