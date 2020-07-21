'''
__init__.py for SUEAP

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np
import abc

class _Individual:
    '''
    A class for representing an individual from a population
    '''

    def __init__(self, x):

        self.x = x

        self.f        = None
        self.S        = None
        self.rank     = None
        self.n        = None
        self.distance = None

    def __lt__(self, other):

        return np.all(self.f < other.f)

    def __str__(self):

        return str(self.f)


def pick(P):
    '''
    Returns a randomly-chosen individual from set P
    '''
    return np.random.choice(tuple(P))

class Problem(metaclass=abc.ABCMeta):
    '''
    A class for multiobjective optimization problems
    '''

    def make_new_pop(self, P, g, G):
        '''
        Standard implementation of make_new_pop:
            - tournament selection
            - crossover
            - mutation
        Inputs:
            P   a population
            g   current generation (for scaling mutation)
            G   total number of generations (for scaling mutation)
        '''
     
        Q = set()

        # goal is N children
        N = len(P)

        # tournament selection
        selected = set()
        for _ in range(N):
            p1 = pick(P)
            p2 = pick(P)
            selected.add(p1 if p1 < p2 else p2)

        # recombination (crossover)
        for _ in range(N):
            child = pick(selected)
            Q.add(_Individual(self.crossover(child, pick(selected)) if np.random.random()<self.pc else child.x))

        # mutation, scaled by fraction of generations passed 
        for q in Q:
            self.mutate(q, g, G)

        return Q


    @abc.abstractmethod
    def eval(p):
        '''
        Evaluates and returns the fitness of individual p.
        Your subclass should override this method.
        '''
        return None
