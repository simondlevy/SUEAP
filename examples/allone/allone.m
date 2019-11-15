function [pops,fits] = allone(popsize, ngen, pc, mu)
% ALLONE  Use SGAP to evolve strings of all 1's.
%
%   [POPS,FITS] = ALLONE(POPSIZE, NGEN, PC, MU)

% create SGAP object
s = sgap(pc, mu);

% create initial population
pop = newpop(s, @randbits, popsize);

% run SGAP on population
[pops,fits] = run(s, pop, ngen);
