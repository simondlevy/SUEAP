'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

from nsga2.algorithms import nsga_ii
import numpy as np
from multiprocessing import Pool, cpu_count
from time import sleep
import abc

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

class _Individual:
    '''
    A class for representing an individual from a population
    '''

    def __init__(self, x):

        self.x = x

        self.f        = None
        self.S        = None
        self.rank     = None
        self.n        = None
        self.distance = None

    def __lt__(self, other):

        return np.all(self.f < other.f)

    def __str__(self):

        return str(self.f)

def pick(P):
    '''
    Returns a randomly-chosen individual from set P
    '''
    return np.random.choice(tuple(P))

class Problem(metaclass=abc.ABCMeta):
    '''
    A class for multiobjective optimization problems
    '''

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
            p1 = pick(P)
            p2 = pick(P)
            selected.add(p1 if p1 < p2 else p2)

        # recombination (crossover)
        for _ in range(N):
            child = pick(selected)
            Q.add(_Individual(self.crossover(child, pick(selected)) if np.random.random()<self.pc else child.x))

        # mutation, scaled by fraction of generations passed 
        for q in Q:
            self.mutate(q, g, G)

        return Q


    @abc.abstractmethod
    def eval(p):
        '''
        Evaluates and returns the fitness of individual p.
        Your subclass should override this method.
        '''
        return None

class NSGA2:

    def __init__(self, problem, N):
        '''
        Inputs:
            problem An object subclassing nsga2.Problem
            N       Population size
        '''
        self.problem = problem
        self.N = N

    def animate(self, G, axes=(0,1), imagename=None):
        '''
        Inputs:
            G          Number of generations
            axes       Axis indices for 2D plot
            imagename  Prefix for image file names
        '''

        from threading import Thread

        plotter = _Plotter(self.problem.fmin, self.problem.fmax, axes, imagename)

        thread = Thread(target=self._run, args=(G, plotter))
        thread.daemon = True
        thread.start()

        # Plot runs on main thread
        plotter.start() 

    def run(self, G):
        '''
        Inputs:
            G Number of generations
        Returns: population after G generations
        '''
        return self._run(G)

    def _run(self, G, plotter):

        P = set([_Individual(self.problem.x()) for _ in range(self.N)])
        self._eval_fits(P)
        Q = set()

        for g in range(G):

            P = nsga_ii(P, Q, self.N, self.problem.fsiz, self.problem.fmin, self.problem.fmax)
            Q = self.problem.make_new_pop(P, g, G)     
            plotter.update(P,g,G)
            sleep(1.0)
            self._eval_fits(Q)
            
    def _eval_fits(self, P):

        P = list(P)

        with Pool(processes=cpu_count()) as pool:

            for p,f in zip(P, pool.map(self.problem.eval, P)):
                p.f = f
