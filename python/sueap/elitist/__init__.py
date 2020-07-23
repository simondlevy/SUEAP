'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from time import time
import numpy as np
from sueap import GA

class Elitist(GA):

    def __init__(self, problem, pop_size, noise_std=0.01, parents_count=10):

        GA.__init__(self, problem, pop_size)

        self.noise_std = noise_std
        self.parents_count = parents_count

    def run(self, ngen, max_fitness=None):
        '''
        Inputs:
            ngen        Number of generations
            max_fitness optional fitness at which to halt
        Returns: fittest individual
        '''

        # Set up communication with workers
        GA.setup_workers(self, ngen)

        # Start with random population
        population = [self.problem.new_params() for _ in range(self.pop_size)]

        # This will store the fittest individual in the population and its fitness
        best = None

        # Loop for specified number of generations (default = inf)
        for gen_idx in range(ngen):

            # Start timer for performance tracking
            t_start = time()

            # Compute fitnesses of current population member
            population, batch_steps = GA.compute_fitness(self, population)

            # Keep the current best in the population
            if best is not None:
                population.append(best)

            # Sort population by fitness
            population.sort(key=lambda p: p[1], reverse=True)

            # Report and store current state
            self._report(population, gen_idx, batch_steps, t_start)

            # Get new best
            best = population[0]

            # Mutate the learnable parameters for each individual in the population
            population = [self.problem.mutate_params(p[0], self.noise_std) for p in population]

            # Quit if maximum fitness reached
            if max_fitness is not None and best[1] >= max_fitness:
                GA.halt_workers(self)
                break

            # Get next population
            population = [population[np.random.randint(self.parents_count)] for _ in range(self.pop_size)]

        # Shut down workers after waiting a little for them to finish
        GA.shutdown_workers(self)

        # Return the fittest individual
        return best[0]

    def _report(self, population, gen_idx, batch_steps, t_start):

        fits = [p[1] for p in population[:self.parents_count]]
        speed = batch_steps / (time() - t_start)
        print('%04d: mean fitness=%+6.2f\tmax fitness=%+6.2f\tstd fitness=%6.2f\tspeed=%d f/s' % (
            gen_idx, np.mean(fits), np.max(fits), np.std(fits), int(speed)))
