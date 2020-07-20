#!/usr/bin/env python3
'''
Use the Neural Engineering framework to solve CartPole via an elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

from sueap import Problem
from sueap.elitist import Elitist

class NefCartpole(Problem):

    def __init__(self, n=10):

        # Encoder
        self.alpha = np.random.uniform(0, 100, n) # tuning parameter alpha
        self.b = np.random.uniform(-20,+20, n)    # tuning parameter b
        self.e = np.random.uniform(-1, +1, (4,n)) # encoder weights

        self.n = n

    def new_params(self):

       return np.random.uniform(-1, +1, (self.n,1)) # decoder weights

    @staticmethod
    def eval(p):
        return None

    @staticmethod
    def mutate(p, g, G):
        return None

    def eval_params(self, params):

        return 0

if __name__ == '__main__':

    e = Elitist(NefCartpole())
    e.run(10)
