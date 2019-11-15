function robj = rmhc(mu, varargin)
% RMHC Random Mutation Hill-Climbing benchmark for evolutionary algorithms
%
% ROBJ = RMHC(MU, [OPTIONS]) takes a mutation rate MU and returns an 
% RMHC object ROBJ.
%
% OPTIONS are:
%
% 'seed', SEED
%  where  SEED is a seed for the random-number generator; this
%  supports reproducible results
%
%  See also RMHC/RUN

robj.mu = mu;

s = sueap(varargin);

robj = class(robj, 'rmhc', s);