function x = mutate(x, mu, gen, ngen)

x = bounded_mutation(x, mu, gen, ngen, -pi, pi);
