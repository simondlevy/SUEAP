function Qt1 = make_new_pop(obj, Pt1, gen, ngen)
% Make child population from parents.  This is a bit of messy glue code
% between NSGA-II and SuEAP.

% goal is N children
N = length(Pt1);

% tournament selection
for i = 1:N
    ix1 = randindex(obj, Pt1);
    ix2 = randindex(obj, Pt1);
    if dominates(Pt1{ix1}, Pt1{ix2})
        selected{i} = Pt1{ix1};
    else
        selected{i} = Pt1{ix2};
    end
end

% recombination (crossover)
for i = 1:N
    if toss(obj, obj.pc)
        child1 = pickrand(obj, selected);
        child2 = pickrand(obj, selected);
        Qt1{i}.genome = crossover(obj, child1.genome, child2.genome);
    else
        Qt1{i}.genome = selected{i}.genome;
    end
end

% mutation, scaled by fraction of generations passed 
for i = 1:N
    Qt1{i}.genome = mutate(Qt1{i}.genome, obj.mu, gen, ngen);
end
