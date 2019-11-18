function member = makemember(i, g, f)
% Population-member constructor for NSGA-II.  Stores index I, genome G,
% and fitness F.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

member = struct('index', i, 'genome', g, 'fitness', f);
