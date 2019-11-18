function b = randbits
% Constructor for ALLONE example.  Returns vector of N random bits.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

N = 10;  % arbitrary

b = rand(1, N) > .5;
