function wheel = roulette(fits)
% make roulette wheel from one-dimensional fitnesses array
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

WHEELSIZE = 10000;

% this should never happen
if max(fits) == min(fits)
    error('Uniform population')
end

% normalize fitnesses
fits = fits - min(fits);
fits = normalize(fits);

% turn fitnesses into wheel index ranges
fits = cumsum(round(WHEELSIZE * fits));

% build wheel
pos = 1;
for i = 1:length(fits)
  wheel(pos:fits(i)) = i;
  pos = fits(i) + 1;
end
