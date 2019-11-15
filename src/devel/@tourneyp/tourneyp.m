function [allpops,allfits] = tourneyp(pop, ngen, theta, mu)
% TOURNEYP Tournament selection in Parallel
%
% ALLPOPS = TOURNEYP(POP, NGEN, THETA, MU) takes a population
% POP, number of generations to be used NGEN, elitism probability THETA
% and mutation rate MU.  It returns a cell array ALLPOPS containing
% the history of the evolved population over NGEN generations.  If MU is 
% given as a decreasing interval, e.g., [1.0 0.1], then mutation rate is by 
% generation, along this interval.
%
% POP  should contain objects belonging to a class or classes that define the 
% following methods:
%
%   FITNESS(OBJ) Returns fitness of OBJ as a scalar or vector
% 
%   MUTATE(OBJ, MU) Returns copy of  OBJ mutated with proability or factor MU 
%
% [ALLPOPS,ALLFITS] = TOURNEYP(POP, NGEN, THETA, MU) also
% returns cell array ALLFITS of fitnesses of each population member in 
% ALLPOPS.
%
% See also FITTEST

% make cell array out of params
funargs = {theta mu};

% run generic SUEAP script
[allpops, allfits] = sueap(pop, ngen, 'tourneyp_update', funargs);
