function pop = newpop(sobj, struname, popsize, varargin)
% NEWPOP Build initial population
%
%   POP = NEWPOP(SOBJ, STRUNAME, POPSIZE) returns a POPSIZE (randomly)
%   initialized cell array of structures built by function name or handle
%   STRUNAME.  SOBJ should be an object that sub-classes SUEAP
%   (MOOP, SGAP, etc.).
%
%   NEWPOP(SOBJ, STRUNAME, POPSIZE, OPTIONS) allows other arguments to
%   be specified for your STRUNAME constructor.
%
%   OPTIONS are:
%
%   'seed', SEED
%    random-number generator seed for reproducible results.
%
%   'data', DATA
%    pass a data block into the contstructor for STRUNAME
% 
%    Note that this option initializes all objects to have the same
%    data contents.  If you want separate data for each object, you
%    should skip NEWPOP and create each object yourself.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% assume no initialization data
data = [];

% get options
for i = 1:length(varargin)
  vararg = varargin{i};
  if ischar(vararg)
    if strcmp(vararg, 'data')
      argval = varargin{i+1};
      data = argval;
      i = i + 1;
    elseif strcmp(vararg, 'seed')
      argval = varargin{i+1};
      seedrandom(sobj, argval);
      i = i + 1;
    end
  end
end

if ~isempty(data)
   for i = 1:popsize
      pop{i} = feval(struname, data);
  end
else
   for i = 1:popsize
      pop{i} = feval(struname);
  end
end



