function [allpops,allfits,sobj] = run(sobj, pop, ngen, varargin)
% RUN Run generations of SGAP algorithm
%
%  [ALLPOPS,ALLFITS] = RUN(SOBJ, POP, NGEN) runs NGEN generations on
%  SGAP object SOBJ (SGAP, SGAP, TOURNEY, et al.), returning cell
%  array of populations ALLPOPS and cell array of their fitnesses
%  ALLFITS.
%
%  RUN(SOBJ, POP, NGEN, POBJ) supports parallel fitness computation
%  through PECON object POBJ.
%
% POP should be a cell aray of structures for which the following
% methods are defined:
%
%   FITNESS(S) Returns fitness of S as a vector
% 
%   MUTATE(S, MU) Returns copy of S mutated with proability or factor MU 
%
%   CROSSOVER(P1, P2) Returns a "child" object made by crossing
%   over "parent" objects P1 and P2

[allpops,allfits] = srun(sobj, pop, ngen, varargin{:});
