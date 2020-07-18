function yn = toss(sobj, p)
% (biased) coin toss
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% no bias
if nargin < 2
  p = 0.5;
end

yn = (rand < p);
