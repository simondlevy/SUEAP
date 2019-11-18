function x = normrand(dims, lo, hi);
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

x = randn(dims) * (hi - lo)/2;
