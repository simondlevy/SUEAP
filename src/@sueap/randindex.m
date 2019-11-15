function index = randindex(sobj, a)
% returns a random index into array A

index = fix(rand * length(a)) + 1;


