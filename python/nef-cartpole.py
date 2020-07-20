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

    @staticmethod
    def eval(p):
        return None

    @staticmethod
    def mutate(p, g, G):
        return None

if __name__ == '__main__':

    e = Elitist(NefCartpole())
    e.run(10)
