function [newpop,sobj] = update(sobj, pop, fits, gen, ngen)
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

% visualize fitnesees if indicated
if ~isempty(sobj.visdims)
    plotfits(fits, sobj.visdims, sobj.vislims, gen, ngen);
end

% fitnesses are in a cell array, but we need a vector
ndims = length(fits{1});
fits = reshape(cell2mat(fits), ndims, length(fits))';

% transpose 1D fitness for (vacuous) dimension collapse
if size(fits, 1) == 1
  fits = fits';
end

% collapse fitnesses to a single dimension
fits = sum(fits, 2);

% make roulette wheel from fitnesses
wheel = roulette(fits);

% keep elite fraction of population
[trash,best] = sort(fits, 'descend');
rankedpop = pop(best);
nelite = fix(sobj.elit * length(pop));
newpop = rankedpop(1:nelite);
  
% fill new population
for i = nelite+1:length(pop)

  % get parents using fitness-proportional selection
  p1 = fpselect(sobj, pop, wheel);
  p2 = fpselect(sobj, pop, wheel);

  % crossover with probbility PC
  if toss(sobj, sobj.pc)

    newpop{i} = crossover(sobj, p1, p2);  

  % otherwise use either parent
  elseif toss(sobj)
    newpop{i} = p1;
  else
    newpop{i} = p2;
  end

  % add mutated offspring to new population
  newpop{i} = mutate(newpop{i}, sobj.mu, gen, ngen);

end

fprintf('\tBest: %f\n', max(fits))


