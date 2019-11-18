function mobj = moop(phi, mu, varargin)
% MOOP Multi-Objective Optimization in Parallel
%
% MOBJ = MOOP(PHI, MU, [OPTIONS]) takes a frontier probability
% PHI and mutation object MU.  It returns a MOOP object MOBJ.
% Frontier probability PHI is the probability that a member of the next 
% generation's population is chosen from the front, instead of from the 
% entire population.  PHI can be either a single value, in which case it 
% stays the same in all generations; or it can be a pair of values, in which 
% case the probability is scaled linearly from the first value to the 
% second over generations
%
% 'elite', ELITISM
%   where ELITISM is the fraction of the next-generation population that comes 
%   from the unmodified "best" current front members without crossover or
%   mutation.  Member A is defined as better than member B if the product of
%   A's fitness values is higher than the product of B's.
%
% 'pc' PC
%   where PC is the probability of crossover (default = 0.0); i.e., the 
%   likelihood that a given member of the frontier will be crossed with 
%   another and replaced by the resulting 'child'
%
% 'seed', SEED
%  where  SEED is a seed for the random-number generator; this
%  supports reproducible results
%
% 'visdims', DIMS
%    where DIMS is  two-dimensional vector of fitness dimensions to 
%    visualize (default axes are determined by fitness values)
%
% 'vislims', LIMS
%    where LIMS is  four-dimensional vector of axis limits for  
%    visualization: [XMIN XMAX YMIN YMAX]
%
% See also MOOP/RUN
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

mobj.phi = phi;
mobj.mu = mu;

s = sueap(varargin);

[mobj.pc, mobj.elite, mobj.visdims,mobj.vislims] = ...
    getopts(s, varargin, {'pc', 'elite', 'visdims', 'vislims'}, ...
            {0.0, 0.0 [], []});

mobj = class(mobj, 'moop', s);


