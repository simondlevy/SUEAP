'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import collections
import numpy as np
import multiprocessing as mp
from time import sleep

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

# Workers use named tuple to send results back to main
WorkerToMainItem = collections.namedtuple('WorkerToMainItem', field_names=['params', 'fitness', 'steps'])

class _Individual:
    '''
    A class to support sorting of individuals in a population
    '''

    def __init__(self, x):

        self.x = x
        self.f = None

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


# Exported classes ----------------------------------------------------------------------------------

class NSGA2:

    def __init__(self, problem, pop_size=100):
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

    def animate(self, ngen, axes=(0,1), imagename=None):
        '''
        Inputs:
            ngen       Number of generations
            axes       Axis indices for 2D plot
            imagename  Prefix for image file names
        '''

        from threading import Thread

        plotter = _Plotter(self.problem.fmin, self.problem.fmax, axes, imagename)

        thread = Thread(target=self._run, args=(ngen, plotter))
        thread.daemon = True
        thread.start()

        # Plot runs on main thread
        plotter.start() 

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

        pop = [self.problem.new_params() for _ in range(self.pop_size)]

        P = set([_Individual(p) for p in pop])
        self._eval_fits(P)

        Q = set()

        for g in range(ngen):

            P = _nsga_ii(P, Q, self.pop_size, self.problem.fsiz, self.problem.fmin, self.problem.fmax)

            Q = self.make_new_pop(P, g, ngen)     

            if plotter is None:
                print('%04d/%04d' % (g+1, ngen))
            else:
                plotter.update(P,g,ngen)
                sleep(1.0)

            self._eval_fits(Q)
            
        self._halt_workers(main_to_worker_queues)

    def _eval_fits(self, P):

        P = list(P)

        with mp.Pool(processes=mp.cpu_count()) as pool:

            for p,f in zip(P, pool.map(self.problem.eval, P)):
                p.f = f

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
 
    def _halt_workers(self, main_to_worker_queues):

        for main_to_worker_queue in main_to_worker_queues:

            main_to_worker_queue.put([])

    def make_new_pop(self, P, g, G):
        '''
        Standard implementation of make_new_pop:
            - tournament selection
            - crossover
            - mutation
        Inputs:
            P   a population
            g   current generation (for scaling mutation)
            G   total number of generations (for scaling mutation)
        '''
     
        Q = set()

        # goal is N children
        N = len(P)

        # tournament selection
        selected = set()
        for _ in range(N):
            p1 = self.pick(P)
            p2 = self.pick(P)
            selected.add(p1 if p1 < p2 else p2)

        # recombination (crossover)
        for _ in range(N):
            child = self.pick(selected)
            Q.add(_Individual(self.problem.crossover(child, self.pick(selected)) if np.random.random()<self.problem.pc else child.x))

        # mutation, scaled by fraction of generations passed 
        for q in Q:
            self.problem.mutate(q, g, G)

        return Q

    def pick(self, P):
        '''
        Returns a randomly-chosen individual from set P
        '''
        return np.random.choice(tuple(P))
