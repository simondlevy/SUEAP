'''
Class implementation for NSGA-II

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np
from time import sleep
from sueap import GA

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
    A class to support sorting of individuals in a population
    '''

    def __init__(self, x, f=None):

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

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        if not self.done:
            return self.ln,

    def update(self, P, g, G):

        P = list(P)
        self.ln.set_data([p.f[self.axes[0]] for p in P], [p.f[self.axes[1]] for p in P])
        self.ax.set_title('%d/%d' % (g+1,G))
        self.g = g
        sleep(0.1)

# Exported classes ----------------------------------------------------------------------------------

class NSGA2(GA):

    def __init__(self, problem, pop_size=100):
        '''
        Inputs:
            problem  An object subclassing nsga2.Problem
            pop_size Population size
        '''
        GA.__init__(self, problem, pop_size)

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

        # Set up communication with workers
        GA.setup_workers(self, ngen)

        # Create initial population and get its fitness
        P = self._eval_fits(set([_Individual(self.problem.new_params()) for _ in range(self.pop_size)]))

        # Create empty child population
        Q = set()

        for g in range(ngen):

            # Run the NSGA-II algorithm on current parents and children, getting new population
            P = _nsga_ii(P, Q, self.pop_size, self.problem.fsiz, self.problem.fmin, self.problem.fmax)

            # Get new child population through selection, mutation, crossover
            Q = self.make_new_pop(P, g, ngen)     

            # Plot or report results
            if plotter is None:
                print('%04d/%04d' % (g+1, ngen))
            else:
                plotter.update(P,g,ngen)

            # Compute child fitnesses on all but last generation (avoids blocking)
            if g<ngen-1:
                Q = self._eval_fits(Q)

        # Shut down workers after waiting a little for them to finish
        GA.shutdown_workers(self)

    def _eval_fits(self, P):

        # Send parameters to workers
        GA.send_params(self, [p.x for p in P])

        # Get back parameter/fitness pairs
        fs, _ = GA.get_fitnesses(self)

        # Rebuild population with fitnesses
        return set([_Individual(x, f) for x,f in fs])

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
            p1 = self._pick(P)
            p2 = self._pick(P)
            selected.add(p1 if p1 < p2 else p2)

        # recombination (crossover) and mutation
        for _ in range(N):
            child = self._pick(selected)
            q = _Individual((self.problem.crossover(child, self._pick(selected)) 
                if np.random.random()<self.problem.pc else child.x))
            self.problem.mutate(q, g, G) # scale mutation by fraction of generations completed
            Q.add(q)

        return Q

    def _pick(self, P):
        '''
        Returns a randomly-chosen individual from set P
        '''
        return np.random.choice(tuple(P))
