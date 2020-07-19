'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

class Elitist:

    def __init__(self, noise_std=0.01, pop_size=2000, parents_count=10, max_gen=None, max_fitness=None):

        self.noise_std = noise_std
        self.pop_size = pop_size
        self.parents_count = parents_count
        self.max_gen = np.iinfo(np.uint32).max if max_gen is None else max_gen
        self.max_fitness = np.inf if max_fitness is None else max_fitness



