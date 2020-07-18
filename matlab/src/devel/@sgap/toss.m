function yn = toss(p)
% (biased) coin toss
% Copyright (c) 2019 Simon D. Levy
%
% MIT License


% no bias
if nargin < 1
  p = 0.5;
end

yn = (rand > p);
