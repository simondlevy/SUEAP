function newpop = sgap_update(pop, fits, gen, ngen, args)

% extract params from args
pc = args{1};
pm = args{2};

% collapse fitnesses to a single dimension
fits = sum(fits, 2);

% report progress
fprintf('Gen: %5d / %-5d \tBest: %f\n', gen, ngen, max(fits))

% make roulette wheel from fitnesses
wheel = roulette(fits);
  
% fill new population
for i = 1:length(pop)

  % get parents using fitness-proportional selection
  p1 = fpselect(pop, wheel);
  p2 = fpselect(pop, wheel);

  % crossover with probbility PC
  if toss(pc)

    newpop(i) = crossover(p1, p2);  

  % otherwise use either parent
  elseif toss
    newpop(i) = p1;
  else
    newpop(i) = p2;
  end

  % add mutated offspring to new population
  newpop(i) = mutate(newpop(i), scalemu(pm, gen, ngen));

end

