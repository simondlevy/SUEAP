function x = randvals(siz, lo, hi)

x = normrand(siz, lo, hi);

x = bound(x, lo, hi);