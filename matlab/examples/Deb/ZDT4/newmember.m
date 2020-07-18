function x = newmember
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

x(1) = bounded_random(0, 1);

x(2:10) = bounded_random(-5, 5);
