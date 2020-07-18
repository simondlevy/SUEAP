function [allpops,allfits,allranks] = run(obj, pop, ngen, varargin)
% RUN Run generations of NSGA-II algorithm
%
%  [ALLPOPS,ALLFITS,ALLRANKS] = RUN(OBJ, POP, NGEN) runs NGEN generations on
%  NSGA2P object OBJ, returning cell array of populations ALLPOPS, a cell
%  array of their fitnesses ALLFITS, and a cell array of their 
%  nondomination ranks ALLRANKS.  There are always NGEN-1 of these, because
%  the initial parent population is empty.
%
%  RUN(OBJ, POP, NGEN, POBJ) supports parallel fitness computation
%  through PECON object POBJ.
%
% POP should be a cell aray of structures for which the following
% methods are defined:
%
%   FITNESS(S) Returns fitness of S as a vector
% 
%   MUTATE(S, MU, SCALEGEN) Returns copy of S mutated with 
%   mutation factor MU and generation fraction SCALEGEN.
%
%   CROSSOVER(P1, P2) Returns a "child" object made by crossing
%   over "parent" objects P1 and P2
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License
  

[allpops,allfits,obj] = srun(obj, pop, ngen, varargin{:});

% XXX we ignore these values and get the elite parent populations, their
% fitnesses, and their ranks
allpops = {{}};
allfits = {{}};
allranks = {{}};
for g = 1:ngen-1
    Pt = obj.Pt{g+1};  % initial parent population is empty
    for i = 1:length(Pt)
        pop{i} = Pt{i}.genome;
        fits{i} = Pt{i}.fitness;
        ranks{i} = Pt{i}.rank;
    end
    allpops{g} = pop;
    allfits{g} = fits;
    allranks{g} = ranks;
end
