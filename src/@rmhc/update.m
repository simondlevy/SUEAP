function newpop = update(robj, pop, fits, gen, ngen)

% first time 'round
if length(pop) == 1
    pop{2} = pop{1};
    fits{2} = fits{1};
end

if fits{2} > fits{1}
    pop{1} = pop{2};
    fits{1} = fits{2};
end

fprintf('Gen: %5d / %-5d \tBest: %f\n', gen, ngen, fits{1})

pop{2} = mutate(pop{1}, robj.mu);

newpop = pop;


