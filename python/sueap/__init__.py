'''
__init__.py for SUEAP

Contains GA superclass for distributed fitness evaluation.

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from time import sleep
import collections
import multiprocessing as mp

# Workers use named tuple to send results back to main
WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

class GA:

    def __init__(self, problem, pop_size):

        self.problem = problem
        self.pop_size = pop_size

        # Use all available CPUs, distributing the population equally among them
        self.workers_count = mp.cpu_count()
        self.evals_per_worker = self.pop_size // self.workers_count

        # Workers will be set up at start of run
        self.main_to_worker_queues = None
        self.worker_to_main_queue = None
        self.workers = None

    def setup_workers(self, ngen):

        self.main_to_worker_queues = []
        self.worker_to_main_queue = mp.Queue(self.workers_count)
        self.workers = []
        for k in range(self.workers_count):
            main_to_worker_queue = mp.Queue()
            self.main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(ngen, k, main_to_worker_queue))
            self.workers.append(w)
            w.start()

    def send_params(self, params):

        for k,queue in enumerate(self.main_to_worker_queues):

            queue.put(params[k*self.evals_per_worker:(k+1)*self.evals_per_worker])

    def get_fitnesses(self):

        batch_steps = 0
        population = []
        pop_size = self.evals_per_worker * self.workers_count
        while len(population) < pop_size:
            item = self.worker_to_main_queue.get()
            population.append((item.params, item.fitness))
            batch_steps += item.steps
        return population, batch_steps
    
    def halt_workers(self):

        for queue in self.main_to_worker_queues:

            queue.put([])

    def shutdown_workers(self):
        sleep(0.25)
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
                self.worker_to_main_queue.put(WorkerToMainItem(params=params, fitness=fitness, steps=steps))
 
