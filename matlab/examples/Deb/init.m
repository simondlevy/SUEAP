function init(n)
% Check number of input arguments to see whether randon-number-generator
% seed has been specified.  If so, we use it to generate the initial 
% population, so that different algorithms can be compared on the same
% initial population.  This does not seed the random-number-generator
% for the algorithm itself.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

if n > 5
    rand('state', 0)
    rand('state', 0)
end
