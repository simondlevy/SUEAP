function mu = scalemu(sobj, gen, ngen)
% Mutation scaled to fraction of generations completed, a la simulated 
% annealing.  Called automatically by SUEAP/UPDATE to scale mutation rate.

smu = getfield(struct(sobj), 'mu');

if length(smu) > 1
    mu = smu(1) + (smu(2) - smu(1))*(gen/ngen);
else
    mu = smu;
end