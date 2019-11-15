function sobj = sgap(pc, mu, varargin)
% SGAP Simple Genetic Algorithm in Parallel
%
% sobj = SGAP(PC, MU, [OPTIONS]) accepts crossover probability PC
% and mutation rate MU.  It returns an SGAP object sobj.
%
% OPTIONS are:
% 
% 'elit', ELITISM
%    where ELITISM is fraction (0-1) of fittest population members preserved
%    as-is into next generation (default = 0)
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
%  See also SGAP/RUN

sobj.mu = mu;
sobj.pc = pc;

s = sueap(varargin);

[sobj.elit,sobj.visdims,sobj.vislims] = getopts(s, varargin, ...
                        {'elit', 'visdims', 'vislims'}, {0, [], []});

sobj = class(sobj, 'sgap', s);


