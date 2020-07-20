'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import time
import os
import pickle
import collections
import numpy as np
import multiprocessing as mp

# Workers use named tuple to send results back to main
WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

class Elitist:

    def __init__(self, problem, pop_size=2000, noise_std=0.01, parents_count=10):

        self.problem = problem
        self.pop_size = pop_size
        self.noise_std = noise_std
        self.parents_count = parents_count

    def run(self, ngen, max_fitness=None):
        '''
        Returns fittest individual.
        '''

        # Use all available CPUs, distributing the population equally among them
        workers_count = mp.cpu_count()
        parents_per_worker = self.pop_size // workers_count

        # Set up communication with workers
        main_to_worker_queues, worker_to_main_queue, workers = self._setup_workers(ngen, workers_count, parents_per_worker)

        # This will store the fittest individual in the population and its fitness
        best = None

        # Loop for specified number of generations (default = inf)
        for gen_idx in range(ngen):

            # Start timer for performance tracking
            t_start = time.time()

            # Get results from workers
            population, batch_steps = self._get_new_population(worker_to_main_queue, parents_per_worker, workers_count)

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
            population = [(self.problem, self.problem.mutate_params(p[0], self.noise_std)) for p in population]

            # Quit if maximum fitness reached
            if max_fitness is not None and best[1] >= max_fitness:
                self._halt_workers(main_to_worker_queues)
                break

            # Send new population to wokers
            self._update_workers(population, main_to_worker_queues, parents_per_worker, self.parents_count)

        # Shut down workers after waiting a little for them to finish
        time.sleep(0.25)
        for w in workers:
            w.join()

        # Return the fittest individual
        return best

    def _setup_workers(self, ngen, workers_count, parents_per_worker):

        main_to_worker_queues = []
        worker_to_main_queue = mp.Queue(workers_count)
        workers = []
        for k in range(workers_count):
            main_to_worker_queue = mp.Queue()
            main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(ngen, k, main_to_worker_queue, worker_to_main_queue))
            workers.append(w)
            w.start()
            main_to_worker_queue.put([(self.problem, self.problem.new_params()) for _ in range(parents_per_worker)])

        return main_to_worker_queues, worker_to_main_queue, workers

    def _worker_func(self, ngen, worker_id, main_to_worker_queue, worker_to_main_queue):

        # Loop over generations, getting parent param dictionaries from main process and mutating to get new population
        for _ in range(ngen):
            parents = main_to_worker_queue.get()
            if len(parents) == 0:
                break
            for solver in parents:
                agent, params = solver
                fitness, steps = self.problem.eval_params(params)
                worker_to_main_queue.put(WorkerToMainItem(params=params, fitness=fitness, steps=steps))
                
    def _get_new_population(self, worker_to_main_queue, parents_per_worker, workers_count):

        batch_steps = 0
        population = []
        pop_size = parents_per_worker * workers_count
        while len(population) < pop_size:
            out_item = worker_to_main_queue.get()
            population.append((out_item.params, out_item.fitness))
            batch_steps += out_item.steps
        return population, batch_steps
    
    def _report(self, population, gen_idx, batch_steps, t_start):

        fits = [p[1] for p in population[:self.parents_count]]
        speed = batch_steps / (time.time() - t_start)
        print('%04d: mean fitness=%+6.2f\tmax fitness=%+6.2f\tstd fitness=%6.2f\tspeed=%d f/s' % (
            gen_idx, np.mean(fits), np.max(fits), np.std(fits), int(speed)))

    def _update_workers(self, population, main_to_worker_queues, parents_per_worker, parents_count):

        for main_to_worker_queue in main_to_worker_queues:

            # Select the fittest parents
            parents = [population[np.random.randint(parents_count)] for _ in range(parents_per_worker)]

            # Send them to workers
            main_to_worker_queue.put(parents)
            
    def _halt_workers(self, main_to_worker_queues):

        for main_to_worker_queue in main_to_worker_queues:

            main_to_worker_queue.put([])


