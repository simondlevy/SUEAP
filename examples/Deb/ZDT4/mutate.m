function x = mutate(x, mu, gen, ngen)

x(1) = bounded_mutation(x(1), gen, ngen, 0, 1);

x(2:end) = bounded_mutation(x(2:end), gen, ngen, -5, 5);
