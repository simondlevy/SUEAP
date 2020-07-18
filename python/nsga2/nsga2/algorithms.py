'''
NSGA-II algorithms

Copyright (C) 2020 Simon D. Levy

MIT License
'''

import numpy as np

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
