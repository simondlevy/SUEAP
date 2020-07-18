function bits = mutate(bits, mu, scalegen)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

bits = xor(bits, rand(size(bits)) < mu);
