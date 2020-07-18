function [allpops,allfits,mobj] = run(mobj, pop, ngen, varargin)
% RUN Run generations of MOOP algorithm
%
%  [ALLPOPS,ALLFITS] = RUN(MOBJ, POP, NGEN, [OPTIONS]) runs NGEN
%  generations on MOOP object MOBJ (MOOP, SGAP, TOURNEY, et al.),
%  returning cell array of populations ALLPOPS and cell array of their
%  fitnesses ALLFITS.
%
% POP should be a cell aray of structures for which the following
% methods are defined:
%
%   FITNESS(S) Returns fitness of S as a vector
% 
%   MUTATE(S, MU) Returns copy of S mutated with proability or
%   factor MU 
%
%   CROSSOVER(P1, P2) Returns a "child" object made by crossing
%   over "parent" objects P1 and P2
%
% OPTIONS are:
%
%   'POBJ', <POBJECT> PECON object for parallelization
%
%   'HFUN', <HALTFUN> halt if HALTFUN returns true on any fitness
%                     of current population.
%
%   'SAVEGEN', <SAVEGEN> Save population every SAVEGEN generations
%
%   'SAVENAME', <SAVENAME> Filename for saving (default = sueap.mat) 
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

[allpops,allfits] = srun(mobj, pop, ngen, varargin{:});
