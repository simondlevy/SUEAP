function yn = toss(sobj, p)
% (biased) coin toss

% no bias
if nargin < 2
  p = 0.5;
end

yn = (rand < p);
