function [allpops,allfits] = sgap(pop, ngen, pc, pm)
% SGAP Simple Genetic Algorithm in Parallel
%
% ALLPOPS = SGAP(POP, NGEN, PC, PM) takes a population
% POP, number of generations to be used NGEN, crossover probability PC,
% mutation proability PM.  It returns a cell array ALLPOPS containing
% the history of the evolved population over NGEN generations.  If PM is 
% given as a decreasing interval, e.g., [1.0 0.1], then mutation rate is 
% scaled generation, along this interval.
%
% POP  should contain objects belonging to a class or classes that define the 
% following methods:
%
%   FITNESS(OBJ) Returns fitness of OBJ as a scalar or vector
% 
%   MUTATE(OBJ, MU) Returns copy of  OBJ mutated with proability or factor MU 
%
%   CROSSOVER(OBJ1, OBJ2) Returns a new object made by crossing OBJ1, OBJ2
%
% [ALLPOPS,ALLFITS] = SGAP(POP, NGEN, PC, PM) also
% returns cell array ALLFITS of fitnesses of each population member in 
% ALLPOPS.
%
% See also FITTEST
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% make cell array out of params
funargs = {pc pm};

% run generic SUEAP script
[allpops, allfits] = sueap(pop, ngen, 'sgap_update', funargs);
