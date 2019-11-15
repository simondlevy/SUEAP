function nobj = nsga2p(pc, mu, varargin)
% NSGA2P Nondominated-Sorting Genetic Algorithm II in Parallel
%
% NOBJ = NSGA2P(PC, MU, [OPTIONS]) accepts crossover probability PC
% and mutation rate MU.  It returns an NSGA2P object NOBJ.
%
% OPTIONS are:
% 
% 'seed', SEED
%    where  SEED is a seed for the random-number generator; this
%    supports reproducible results
%
% 'visdims', DIMS
%    where DIMS is  two-dimensional vector of fitness dimensions to 
%    visualize (default axes are determined by fitness values)
%
% 'vislims', LIMS
%    where LIMS is  four-dimensional vector of axis limits for  
%    visualization: [XMIN XMAX YMIN YMAX]
%
%  See also NSGA2P/RUN

% store params
nobj.mu = mu;
nobj.pc = pc;

% NSGA-II requires storing population of parents and their fitnesses on 
% each generation t.
nobj.Pt = {{}};

s = sueap(varargin);

[nobj.visdims, nobj.vislims] = getopts(s, varargin, ...
    {'visdims', 'vislims'}, {[], []});

nobj = class(nobj, 'nsga2p', s);


