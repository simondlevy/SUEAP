function newpop = sgap_update(pop, fits, gen, ngen, args)

% extract params from args
theta = args{1};
mu = args{2};

[newpop(1), bestfit] = fittest(pop, fits);

fprintf('Gen: %5d / %-5d \tBest: %f\n', gen, ngen, bestfit)

for j = 2 : length(pop)
  c1 = randindex(pop);
  c2 = randindex(pop);
  if sum(fits(c1,:)) > sum(fits(c2,:))
    better = c1;
    worse = c2;
  else
    better = c2;
    worse = c1;
  end

  if rand < theta
    newpop(j) = pop(better);
  else
    newpop(j) = pop(worse);
  end
end
  
for j = 2:length(newpop)
    newpop(j) = mutate(newpop(j), scalemu(mu, gen, ngen));
end
