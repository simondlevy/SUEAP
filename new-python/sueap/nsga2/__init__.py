'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import abc

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
