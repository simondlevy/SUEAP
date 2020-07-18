function [winner,maxfit] = fittest(pop, fits)
% WINNER return fittest member of population
%
% WINNER = FITTEST(POP, FITS) takes population POP and its fitnesses FITS and
% returns element of POP with highest fitness.  Handles multi-dimensional
% fitness by taking mean over dimensions.
%
% [WINNER,MAXFIT] = FITTEST(POP, FITS) also returns winner's fitness
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

maxfit = -Inf;

for i = 1:length(pop)
    f = sum(fits(i,:));
    if f > maxfit
        maxfit = f;
        winner = pop(i);
    end
end



