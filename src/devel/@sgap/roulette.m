function wheel = roulette(fits)
% make roulette wheel from one-dimensional fitnesses array
%
%     Copyright (c) 2019 Simon D. Levy
%
%     MIT License

% normalize fitnesses
fits = fits - min(fits);
fits = normalize(fits);

% get size of wheel based on smallest difference
fits = fits + min(fits(find(fits)));
fits = normalize(fits);
n = ceil(1 / min(fits));

% turn fitnesses into wheel index ranges
fits = cumsum(round(n * fits));

% build wheel
pos = 1;
for i = 1:length(fits)
  wheel(pos:fits(i)) = i;
  pos = fits(i) + 1;
end
