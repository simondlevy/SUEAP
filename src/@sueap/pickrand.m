function el = pickrand(sobj, a)
% returns a random element of array A

ix = randindex(sobj, a);
if iscell(a)
    el = a{ix};
else
    el = a(ix);
end


