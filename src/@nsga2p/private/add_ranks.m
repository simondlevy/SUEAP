function F = add_ranks(F, i)
% include the rank of each member of a non-dominated front along with the
% member's fitness and genome

for j = 1:length(F)
    F{j}.rank = i;
end