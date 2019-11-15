function child = stcross(sobj, parent1, parent2)
% STCROSS   Structural crossover
%     CHILD = STRCROSS(SOBJ, PARENT1, PARENT2) performs produces CHILD
%     having same fields as PARENT1, PARENT2.  The value of a given
%     field for CHILD is determined by flipping a coin and selecting
%     the value of that field from either PARENT1 or PARENT2.  If
%     parents do not have identical field names, an error is thrown.
%     SOBJ is a SUEAP object (MOOP object, SGAP object, etc.).

fn1 = fieldnames(parent1);
fn2 = fieldnames(parent2);
fn = intersect(fn1, fn2);

if length(fn) ~= length(fn1) | length(fn) ~= length(fn2)
  error('Parents must have identical field names')
end

child = [];

for k = 1:length(fn)
  if rand > 0.5
    parent = parent1;
  else
    parent = parent2;
  end
  child = setfield(child, fn{k}, getfield(parent, fn{k}));
end



