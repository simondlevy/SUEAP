function x = bound(x, lo, hi)
% keep random values in bounds

x = max(x, lo);

x = min(x, hi);