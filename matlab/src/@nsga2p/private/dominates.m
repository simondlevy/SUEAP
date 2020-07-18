function yesno = dominates(p, q)
% returns true if population member p dominates member q, false otherwise
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

yesno = logical(prod(double(p.fitness > q.fitness)));
