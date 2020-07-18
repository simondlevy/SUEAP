function [pops,fits] = fon(algo, popsize, ngen, pc_or_phi, mu, seed)
% FON  Fonseca & Fleming's non-convex multi-objective optimization
% problem for testing NSGA-II.  
%
% FON(ALGORITHM, POPSIZE, NGEN, PC_OR_PHI, MU, [SEED])
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

init(nargin)

obj = feval(algo, pc_or_phi, mu, ...
    'visdims', [1 2], 'vislims', [-1 0 -1 0]);

pop = newpop(obj, @newmember, popsize);

run(obj, pop, ngen);
