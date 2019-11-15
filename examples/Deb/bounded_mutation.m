function x = bounded_mutation(x, mu, gen, ngen, lo, hi)
% mutate genome values a la simulated annealing and keep mutated values in 
% bounds

mu = mu*((ngen-gen)/ngen);

x = x + mu * normrand(size(x), lo, hi);

x = bound(x, lo, hi);

