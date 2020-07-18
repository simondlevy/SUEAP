function newpop = remove(pop, subpop)
% Remove sub-population.  Instead of comparing members by their contents,
% or keeping a separate list of member indices, we store an index in each
% population member.  Member identity then equals index identity.
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

newinds = setdiff(getinds(pop), getinds(subpop));

newpop = {};

for i = 1:length(pop)
    if find(pop{i}.index == newinds)
        newpop{end+1} = pop{i};
    end
end

function inds = getinds(pop)
inds = zeros(1, length(pop));
for i = 1:length(pop)
    inds(i) = pop{i}.index;
end
  
    
