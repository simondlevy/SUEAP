function yn = toss(p)
% (biased) coin toss

% no bias
if nargin < 1
  p = 0.5;
end

yn = (rand > p);
