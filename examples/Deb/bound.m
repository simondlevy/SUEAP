function x = bound(x, lo, hi)
% keep random values in bounds
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

x = max(x, lo);

x = min(x, hi);
