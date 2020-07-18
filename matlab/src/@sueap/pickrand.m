function el = pickrand(sobj, a)
% returns a random element of array A
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

ix = randindex(sobj, a);
if iscell(a)
    el = a{ix};
else
    el = a(ix);
end


