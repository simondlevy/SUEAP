'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import abc

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

def nsga_ii(P, Q, N, fsiz, fmin, fmax):

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
