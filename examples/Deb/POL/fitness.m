function f = fitness(x)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

A1 = 0.5*sin(1) - 2*cos(1) + sin(2) + 1.5*cos(2);
A2 = 1.5*sin(1) - cos(1) + 2*sin(2) - 0.5*cos(2);

x1 = x(1);
x2 = x(2);

B1 = 0.5*sin(x1) - 2*cos(x1) + sin(x2) + 1.5*cos(x2);
B2 = 1.5*sin(x1) - cos(x1) + 2*sin(x2) - 0.5*cos(x2);

f(1) = 1 + (A1 - B1)^2 + (A2 - B2)^2;
f(2) = (x1 + 3)^2 + (x2 + 1)^2;

% we're supposed to minimize
f = -f;
