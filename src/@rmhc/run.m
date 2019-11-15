function [allpops,allfits,robj] = run(robj, stru, ngen, varargin)
% RUN Run generations of RMHC algorithm
%
%  [ALLPOPS,ALLFITS] = RUN(ROBJ, STRU, NGEN) runs NGEN generations on
%  structure STRU using RMHC object ROBJ. Returns cell array of evolved 
%  structures ALLSTRUS and cell array of their fitnesses ALLFITS.
%
%
% STRU should be a data structure for which the following
% methods are defined:
%
%   FITNESS(STRU) Returns fitness of S as a vector
% 
%   MUTATE(STRU, MU) Returns copy of S mutated with proability or factor MU 

pop{1} = stru;

[allpops,allfits] = srun(robj, pop, ngen, varargin{:});
