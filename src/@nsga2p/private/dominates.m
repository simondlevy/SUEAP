function yesno = dominates(p, q)
% returns true if population member p dominates member q, false otherwise

yesno = logical(prod(double(p.fitness > q.fitness)));