function f = fitness(x)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

f(1) = x(1);

g = 1 + 10*(n-1) + sum(x(2:end).^2 - 10*cos(4*pi*x(2:end)));

f(2) = g*(1 - sqrt(x(1)/g)); 

% we're supposed to minimize
f = -f;
