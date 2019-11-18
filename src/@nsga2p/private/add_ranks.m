function F = add_ranks(F, i)
% include the rank of each member of a non-dominated front along with the
% member's fitness and genome
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

for j = 1:length(F)
    F{j}.rank = i;
end
