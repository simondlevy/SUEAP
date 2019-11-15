function [pops,fits] = zdt4(algo, popsize, ngen, pc_or_phi, mu, seed)
% ZDT4 : Zitzler, Deb, and Thiele's fourth multi-objective optimization 
% problem for testing NSGA-II.  
%
% ZDT4(ALGORITHM, POPSIZE, NGEN, PC_OR_PHI, MU, [SEED])

init(nargin)

obj = feval(algo, pc_or_phi, mu, ...
    'visdims', [1 2], 'vislims', [-1 0 -1 0]);
    
pop = newpop(obj, @newmember, popsize);

run(obj, pop, ngen);
