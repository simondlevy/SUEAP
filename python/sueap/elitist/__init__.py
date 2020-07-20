'''
Class implementation for a simple elitist GA

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import collections
import multiprocessing as mp

class Elitist:

    # Workers use named tuple to send results back to main
    WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'reward', 'steps'])

    def __init__(self, problem, pop_size=2000, noise_std=0.01, parents_count=10):

        self.problem = problem
        self.pop_size = pop_size
        self.noise_std = noise_std
        self.parents_count = parents_count

    def run(self, ngen):

        # Use all available CPUs, distributing the population equally among them
        workers_count = mp.cpu_count()
        parents_per_worker = self.pop_size // workers_count

        # Set up communication with workers
        main_to_worker_queues, worker_to_main_queue, workers = self._setup_workers(ngen, workers_count, parents_per_worker)

        '''
        # This will store the fittest individual in the population and its reward
        best = None
        best_reward = None

        # Loop for specified number of generations (default = inf)
        for gen_idx in range(args.max_gen):

            # Start timer for performance tracking
            t_start = time.time()

            # Get results from workers
            population, batch_steps = get_new_population(worker_to_main_queue, parents_per_worker, workers_count)

            # Keep the current best in the population
            if best is not None:
                population.append(best)

            # Sort population by reward (fitness)
            population.sort(key=lambda p: p[1], reverse=True)

            # Report and store current state
            report(population, args.parents_count, gen_idx, batch_steps, t_start)

            # Get new best
            best = population[0]

            # Save best if it's better than previous
            if save_path is not None:
                best_reward = save_best(save_path, best[0], best[1], best_reward, agent)

            # Mutate the learnable parameters for each individual in the population
            population = [(agent, agent.mutate_params(p[0], args.noise_std)) for p in population]

            # Quit if maximum reward reached
            if args.max_reward is not None and best_reward >= args.max_reward:
                halt_workers(main_to_worker_queues)
                break

            # Send new population to wokers
            update_workers(population, main_to_worker_queues, parents_per_worker, args.parents_count)

        # Shut down workers after waiting a little for them to finish
        time.sleep(0.25)
        for w in workers:
            w.join()
        '''

    def _setup_workers(self, ngen, workers_count, parents_per_worker):

        main_to_worker_queues = []
        worker_to_main_queue = mp.Queue(workers_count)
        workers = []
        for k in range(workers_count):
            main_to_worker_queue = mp.Queue()
            main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(self, ngen, k, main_to_worker_queue, worker_to_main_queue))
            workers.append(w)
            #w.start()
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
                fitness, steps = self.paroblem.eval_params(params)
                worker_to_main_queue.put(self.WorkerToMainItem(params=params, fitness=fitness, steps=steps))
