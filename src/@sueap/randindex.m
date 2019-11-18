function index = randindex(sobj, a)
% returns a random index into array A
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

index = fix(rand * length(a)) + 1;


