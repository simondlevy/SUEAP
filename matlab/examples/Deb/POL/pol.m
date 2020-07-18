function [pops,fits] = pol(algo, popsize, ngen, pc_or_phi, mu, seed)
% POL  Poloni's non-convex, disconnected multi-objective optimization
% problem for testing NSGA-II.
%
% POL(ALGORITHM, POPSIZE, NGEN, PC_OR_PHI, MU, [SEED])
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

init(nargin)

m = feval(algo, pc_or_phi, mu, ...
    'visdims', [1 2], 'vislims', [-1 0 -1 0]);

pop = newpop(m, @newmember, popsize);

run(m, pop, ngen);
