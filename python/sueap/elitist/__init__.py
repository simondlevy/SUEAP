'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

class Elitist:

    def __init__(self, problem, pop_size=2000, noise_std=0.01, parents_count=10):

        self.problem = problem
        self.pop_size = pop_size
        self.noise_std = noise_std
        self.parents_count = parents_count

    def run(self, G):

        return





