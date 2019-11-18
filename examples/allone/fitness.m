function result = fitness(bits)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% for SGAP
result = sum(bits) / length(bits);

% for MOOP
%result = double(bits);
