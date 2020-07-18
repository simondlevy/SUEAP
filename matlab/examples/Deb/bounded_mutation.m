function x = bounded_mutation(x, mu, gen, ngen, lo, hi)
% mutate genome values a la simulated annealing and keep mutated values in 
% bounds
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

mu = mu*((ngen-gen)/ngen);

x = x + mu * normrand(size(x), lo, hi);

x = bound(x, lo, hi);

