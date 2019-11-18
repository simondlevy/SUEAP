function x = mutate(x, mu, gen, ngen)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

x = bounded_mutation(x, mu, gen, ngen, -pi, pi);
