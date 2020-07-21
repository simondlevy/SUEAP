'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import time
import collections
import numpy as np
import multiprocessing as mp

# Algorithms ---------------------------------------------------------------------------------------

def _fast_non_dominated_sort(P):

    F = [set()] # Fronts

    for p in P:
        p.S = set()
        p.n = 0
        for q in P:
            if p < q:                # If p dominates q
                p.S.add(q)           # Add q to the set of solutions dominated by p
            elif q < p:
                p.n += 1             # Increment the domination counter of p
        if p.n == 0:                 # p belongs to the first front
            p.rank = 1
            F[0].add(p)
    i = 0                            # Initialize the front counter
    while len(F[i]) > 0:
        Q = set()                    # Used to store the members of the next front
        for p in F[i]:
            for q in p.S:
                q.n -= 1
                if q.n == 0:         # q belongs to the next front
                    q.rank = i+1
                    Q.add(q)
        i += 1
        F.append(Q)

    return F[:-1]

def _crowding_distance_assignment(I, fsiz, fmin, fmax):

    for p in I:                                  # initialize distance
        p.distance = 0

    for m in range(fsiz):                        # for each objective m
        I = sorted(I, key=lambda self:self.f[m]) # sort using each objective value
        I[0].distance = I[-1].distance = np.inf  # so that boundary points always selected
        for i in range(1,len(I)-1):              # for all other points
            I[i].distance += (I[i+1].f[m] - I[i-1].f[m]) /(fmax[m] - fmin[m])

def _nsga_ii(P, Q, N, fsiz, fmin, fmax):

    # Core algorithm from Deb et al. (2002)
    R = list(P.union(Q))                                            # Combine parent and offspring population
    F = _fast_non_dominated_sort(R)                                 # F = (F_1, F_2, ...), all nondominated fronts of R_t
    P, i = set(), 0
    while (len(P) + len(F[i])) < N:                                 # Until the parent population is filled
        _crowding_distance_assignment(list(F[i]), fsiz, fmin, fmax) # Calculate crowding-distance in F_i
        P = P.union(F[i])                                           # Include ith nondominated front in the parent pop
        i += 1                                                      # Check the next front for inclusion
    F[i] = sorted(F[i], key=lambda self:self.n)                     # Sort in descending order using <_n
    P = P.union(F[i][:(N-len(P))])                                  # Choose the first (N-|P_{t+1}) elements of F_i

    return P

# Internal classes ----------------------------------------------------------------------------------

class _Individual:
    '''
    A class for representing an individual from a population
    '''

    def __init__(self, x, f):

        self.x = x
        self.f = f

        self.S        = None
        self.rank     = None
        self.n        = None
        self.distance = None

    def __lt__(self, other):

        return np.all(self.f < other.f)

    def __str__(self):

        return str((self.x, self.f))


class _Plotter:
    '''
    A class for animated 2D fitness plots
    '''

    def __init__(self, fmin, fmax, axes, imagename):

        import matplotlib.pyplot as plt

        self.fig, self.ax = plt.subplots()
        self.ln, = plt.plot([], [], 'r.')
        self.ax.set_xlim((fmin[0], fmax[0]))
        self.ax.set_ylim((fmin[1], fmax[1]))
        self.ax.set_xlabel('$f_%d$' % axes[0])
        self.ax.set_ylabel('$f_%d$' % axes[1])
        self.ax.set_aspect('equal')

        self.imagename = imagename
        self.g = None
        self.gprev = None
        self.plt = plt
        self.axes = axes
        self.ani = None
        self.done = False

    def start(self):

        from matplotlib.animation import FuncAnimation

        self.ani = FuncAnimation(self.fig, self._animate, blit=False)
        self.plt.show()

    def _animate(self, _):

        if self.imagename is not None:
            if self.g is not None:
                if self.g != self.gprev:
                    self.plt.savefig('%s_%04d.png' % (self.imagename, self.g))
                    self.gprev = self.g

        if not self.done:
            return self.ln,

    def update(self, P, g, G):

        P = list(P)
        self.ln.set_data([p.f[self.axes[0]] for p in P], [p.f[self.axes[1]] for p in P])
        self.ax.set_title('%d/%d' % (g+1,G))
        self.g = g


# Named tuple used by workers to send results back to main ------------------------------------------

WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

# Exported classes ----------------------------------------------------------------------------------

class NSGA2:

    def __init__(self, problem, pop_size=2000):
        '''
        Inputs:
            problem  An object subclassing nsga2.Problem
            pop_size Population size
        '''
 
        self.problem = problem
        self.pop_size = pop_size

        # Use all available CPUs, distributing the population equally among them
        self.workers_count = mp.cpu_count()
        self.parents_per_worker = self.pop_size // self.workers_count

    def run(self, ngen):
        '''
        Inputs:
            ngen Number of generations
        Returns: population after ngen generations
        '''
        return self._run(ngen)

    def _run(self, ngen, plotter=None):

        # Set up communication with workers and send them the initial population
        main_to_worker_queues, worker_to_main_queue, workers = self._setup_workers(ngen)

        # Create initially empty child population
        Q = set()

        # Loop for specified number of generations (default = inf)
        for gen_idx in range(ngen):

            # Start timer for performance tracking
            #t_start = time.time()

            # Get results from workers
            population, batch_steps = self._get_new_population(worker_to_main_queue)

            # Combine parameters and fitnesses to work with NSGA-II algorithm
            P = set([_Individual(p[0], p[1]) for p in population])

            # Run NSGA-II
            P = _nsga_ii(P, Q, self.pop_size, self.problem.fsiz, self.problem.fmin, self.problem.fmax)

            Q = self.problem.make_new_pop(P, gen_idx, ngen)     

            break

            if plotter is None:
                print('%04d/%04d' % (gen_idx+1, ngen))
            else:
                plotter.update(P,gen_idx,ngen)
                time.sleep(1.0)
 
            # Send new population to workers
            self._update_workers(P, main_to_worker_queues)

        # Shut down workers after waiting a little for them to finish
        time.sleep(0.25)
        for w in workers:
            w.join()

        # Return the first front
        return None # XXX

    def _setup_workers(self, ngen):

        main_to_worker_queues = []
        worker_to_main_queue = mp.Queue(self.workers_count)
        workers = []
        for k in range(self.workers_count):
            main_to_worker_queue = mp.Queue()
            main_to_worker_queues.append(main_to_worker_queue)
            w = mp.Process(target=self._worker_func, args=(ngen, k, main_to_worker_queue, worker_to_main_queue))
            workers.append(w)
            w.start()
            main_to_worker_queue.put([self.problem.new_params() for _ in range(self.parents_per_worker)])

        return main_to_worker_queues, worker_to_main_queue, workers

    def _worker_func(self, ngen, worker_id, main_to_worker_queue, worker_to_main_queue):

        # Loop over generations, getting parent param dictionaries from main process and mutating to get new population
        for _ in range(ngen):
            parents = main_to_worker_queue.get()
            if len(parents) == 0: # main sends [] when done
                break
            for parent in parents:
                fitness, steps = self.problem.eval_params(parent)
                worker_to_main_queue.put(WorkerToMainItem(params=parent, fitness=fitness, steps=steps))
                
    def _get_new_population(self, worker_to_main_queue):

        batch_steps = 0
        population = []
        pop_size = self.parents_per_worker * self.workers_count
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

    def _update_workers(self, population, main_to_worker_queues):

        for main_to_worker_queue in main_to_worker_queues:

            # Select the fittest parents
            parents = [population[np.random.randint(self.parents_count)] for _ in range(self.parents_per_worker)]

            # Send them to workers
            main_to_worker_queue.put(parents)
            
    def _halt_workers(self, main_to_worker_queues):

        for main_to_worker_queue in main_to_worker_queues:

            main_to_worker_queue.put([])


