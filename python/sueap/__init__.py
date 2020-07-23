'''
__init__.py for SUEAP

Contains GA superclass for distributed fitness evaluation.

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import time
import collections
import multiprocessing as mp

# Workers use named tuple to send results back to main
_WorkerToMainItem = collections.namedtuple('_WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

class GA:
    '''
    GA superclass for distributed fitness evaluation.
    '''

    def __init__(self, problem, pop_size):
        '''
        Inputs:
            problem  an object providing new_params() and eval_params() methods
            pop_size population size
        '''
 
        self.problem = problem
        self.pop_size = pop_size

        # Use all available CPUs, distributing the population equally among them
        self.workers_count = mp.cpu_count()

        # Workers will be set up at start of run
        self.main_to_worker_queues = None
        self.worker_to_main_queue = None
        self.workers = None

    def start_workers(self, ngen):
        '''
        Starts the workers for evaluating sub-population fitnesses.
        Inputs:
            ngen number of generations to run
        '''
 
        self.main_to_worker_queues = []
        self.worker_to_main_queue = mp.Queue(self.workers_count)
        self.workers = []
        for k in range(self.workers_count):
            main_to_worker_queue = mp.Queue()
            self.main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(ngen, k, main_to_worker_queue))
            self.workers.append(w)
            w.start()

    def compute_fitness(self, params):
        '''
        Sends sub-populations to workers to compute fitness.
        Inputs:
            params list of arrays of parameters from each population member
        Returns: 
            a list of pairs of the form (params,fitness), one for each population member
            a count of the number of evaluation steps taken to compute the fitness
        '''
 
        population = []
        steps = 0

        # Compute size of sub-populations
        evals_per_worker = self.pop_size // self.workers_count

        # Send sub-populations to workers
        for k,queue in enumerate(self.main_to_worker_queues):
            queue.put(params[k*evals_per_worker:(k+1)*evals_per_worker])

        # Get back population fitnesses and number of steps taken to compute
        pop_size = evals_per_worker * self.workers_count
        while len(population) < pop_size:
            item = self.worker_to_main_queue.get()
            population.append((item.params, item.fitness))
            steps += item.steps

        # Evaulate remaining population members on main host
        for p in params[pop_size:self.pop_size]:
            f, s = self.problem.eval_params(p)
            population.append((p,f))
            steps += s

        return population, steps
    
    def halt_workers(self):
        '''
        Halts workers before they have completed the specified number of generations; for example, when
        a desired maximum fitness has been achieved.
        '''
        for queue in self.main_to_worker_queues:

            queue.put([])

    def shutdown_workers(self):
        '''
        Shuts down workers after pausing a brief interval for them to complete.
        '''
        time.sleep(0.25)
        for w in self.workers:
            w.join()

    def _worker_func(self, ngen, worker_id, main_to_worker_queue):

        # Loop over generations, getting params, evaluating their fitnesses, and sending them back to main
        for _ in range(ngen):
            allparams = main_to_worker_queue.get()
            if len(allparams) == 0: # main sends [] when done
                break
            for params in allparams:
                fitness, steps = self.problem.eval_params(params)
                self.worker_to_main_queue.put(_WorkerToMainItem(params=params, fitness=fitness, steps=steps))
 
