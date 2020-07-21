#!/usr/bin/env python3
'''
Use NSGS-II to solve multiobjective fitness problem from Fonseca and Fleming (1993)

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

from sueap import Problem, pick
from sueap.tmp import NSGA2

class Fon:

    PM   = .01
    PC   = .7

    def new_params(self):
        return 8 * np.random.random(3) - 4

    def eval_params(self, x):
        return np.array((1 - np.exp(-np.sum((x-1/np.sqrt(3))**2)), (1 - np.exp(-np.sum((x+1/np.sqrt(3))**2))))), 1

    def mutate(self, x, g, G):
        return x + np.random.randn(3) * Fon.PM * (G-g)/G

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

    def make_new_pop(self, P, g, G):
        '''
        Standard implementation of make_new_pop:
            - tournament selection
            - crossover
            - mutation
        Inputs:
            P     a population of individuals with the < relation defined
            g     current generation (for scaling mutation)
            ngen  total number of generations (for scaling mutation)
        Returns: params for a new population
        '''
     
        # goal is N children
        N = len(P)
        Qparams = [None]*N

        # tournament selection
        selected = set()
        for _ in range(N):
            p1 = pick(P)
            p2 = pick(P)
            selected.add(p1 if p1 < p2 else p2)

        # recombination (crossover)
        for k in range(N):
            child = pick(selected)
            Qparams[k] = self.crossover(child, pick(selected)) if np.random.random()<self.pc else child.x
            Qparams[k] = self.mutate(Qparams[k], g, G)

        return Qparams

if __name__ == '__main__':

    np.random.seed(0)

    nsga2 = NSGA2(Fon(), 8)
    #nsga2.animate(30)
    nsga2.run(1)
