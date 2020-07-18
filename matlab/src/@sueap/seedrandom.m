function seedrandom(sobj, seed)
% seed the random-number generators
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

rand('state', seed)
randn('state', seed)
