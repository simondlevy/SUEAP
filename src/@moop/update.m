function [newpop,mobj] = update(mobj, pop, fits, gen, ngen)
% get next population and front based on fitness of current pop.

% separate the frontier elements in a separate data structure
[front,notfront] = getfront(mobj, fits);

% start with empty new front
newfront = [];

% scale frontier-preference probability by generation if specified 
if length(mobj.phi) > 1
    phi = (mobj.phi(2) - mobj.phi(1)) * (gen/ngen) + mobj.phi(1);
else
    phi = mobj.phi;
end

% compute number of next-generation members to keep as elites
nelite = mobj.elite * length(pop);
neliteallow=min(ceil(nelite),length(front));

% choose population members until the next population is full, leaving room
% for the elites
for i = 1:length(pop)-neliteallow

    % is new guy on front?
    on_front = false;

    % if FRONT is empty, pick only from the NOTFRONT
    if isempty(front)
        index = pickrand(mobj, notfront);
    else % frontier is not empty
        if toss(mobj, phi) || isempty(notfront)
            % pick from FRONT with PHI probability
            % if NOTFRONT is empty, always pick from FRONT
            index = pickrand(mobj, front);
            on_front = true;
        else % pick from entire population with (1-PHI) probability
            index = pickrand(mobj, [front notfront]);
        end
    end

    % adding the item to the new population NEWPOP
    newpop{i} = pop{index};
 
end

% run crossover (sexual recombination) on the next population: each pop.
% member is crossed with a randomly picked member and replaced with the
% resulting child
for i = 1:length(newpop)
    if toss(mobj, mobj.pc)
        parent1 = newpop{i};
        parent2 = pickrand(mobj, newpop);
        newpop{i} = crossover(mobj, parent1, parent2);
    end
end

% mutate the next population
for i = 1:length(newpop)
    newpop{i} = mutate(newpop{i}, mobj.mu, gen, ngen);
end

% rank frontier members by fitness product across fitness dimensions
frontfits = fits(front)';
frontfitprods = prod(cell2mat(frontfits), 2);
[dummy, frontranks] = sort(frontfitprods,'descend');

% fill remaining population with unmodified frontier elites
% build an index of front members
for i = 1:neliteallow
%     add the frontier elites in a lowest to hightest order
%     such that newpop{end} has the highest fitness product
    newpop{end+1} = pop{front(frontranks(neliteallow+1-i))};   
end

% report progress
fprintf('\tFront: %5d / %-5d\n', length(front), length(newpop))

% visualize fitnesses if indicated
if ~isempty(mobj.visdims)
    plotfront(fits, front, notfront, mobj.visdims, mobj.vislims, gen, ngen);
end


