'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import time
import collections
import numpy as np
import multiprocessing as mp

# Workers use named tuple to send results back to main
WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

class Elitist:

    def __init__(self, problem, pop_size=2000, noise_std=0.01, parents_count=10):

        self.problem = problem
        self.pop_size = pop_size

        # Use all available CPUs, distributing the population equally among them
        self.workers_count = mp.cpu_count()
        self.evals_per_worker = self.pop_size // self.workers_count

        # Workers will be set up at start of run
        self.main_to_worker_queues = None
        self.worker_to_main_queue = None
        self.workers = None

        self.noise_std = noise_std
        self.parents_count = parents_count

    def run(self, ngen, max_fitness=None):
        '''
        Returns fittest individual.
        '''

        # Set up communication with workers
        self._setup_workers(ngen)

        # Send initial population parameters
        self._send_params([self.problem.new_params() for _ in range(self.pop_size)])

        # This will store the fittest individual in the population and its fitness
        best = None

        # Loop for specified number of generations (default = inf)
        for gen_idx in range(ngen):

            # Start timer for performance tracking
            t_start = time.time()

            # Get results from workers
            population, batch_steps = self._get_fitnesses()

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
                self._halt_workers()
                break

            # Send new population to workers
            self._send_params([population[np.random.randint(self.parents_count)] for _ in range(self.pop_size)])

        # Shut down workers after waiting a little for them to finish
        self._shutdown_workers()

        # Return the fittest individual
        return best[0]

    def _report(self, population, gen_idx, batch_steps, t_start):

        fits = [p[1] for p in population[:self.parents_count]]
        speed = batch_steps / (time.time() - t_start)
        print('%04d: mean fitness=%+6.2f\tmax fitness=%+6.2f\tstd fitness=%6.2f\tspeed=%d f/s' % (
            gen_idx, np.mean(fits), np.max(fits), np.std(fits), int(speed)))

    def _setup_workers(self, ngen):

        self.main_to_worker_queues = []
        self.worker_to_main_queue = mp.Queue(self.workers_count)
        self.workers = []
        for k in range(self.workers_count):
            main_to_worker_queue = mp.Queue()
            self.main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(ngen, k, main_to_worker_queue))
            self.workers.append(w)
            w.start()

    def _send_params(self, params):

        for k,queue in enumerate(self.main_to_worker_queues):

            queue.put(params[k*self.evals_per_worker:(k+1)*self.evals_per_worker])

    def _worker_func(self, ngen, worker_id, main_to_worker_queue):

        # Loop over generations, getting params, evaluating their fitnesses, and sending them back to main
        for _ in range(ngen):
            allparams = main_to_worker_queue.get()
            if len(allparams) == 0: # main sends [] when done
                break
            for params in allparams:
                fitness, steps = self.problem.eval_params(params)
                self.worker_to_main_queue.put(WorkerToMainItem(params=params, fitness=fitness, steps=steps))
                
    def _get_fitnesses(self):

        batch_steps = 0
        population = []
        pop_size = self.evals_per_worker * self.workers_count
        while len(population) < pop_size:
            out_item = self.worker_to_main_queue.get()
            population.append((out_item.params, out_item.fitness))
            batch_steps += out_item.steps
        return population, batch_steps
    
    def _halt_workers(self):

        for queue in self.main_to_worker_queues:

            queue.put([])

    def _shutdown_workers(self):
        time.sleep(0.25)
        for w in self.workers:
            w.join()


