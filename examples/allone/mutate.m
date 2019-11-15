function bits = mutate(bits, mu, scalegen)

bits = xor(bits, rand(size(bits)) < mu);
