function e = fpselect(sobj, pop, wheel)
% select element of population member using fitness-proportional roulette wheel
%
% Copyright (c) 2019 Simon D. Levy
%
% MIT License

e = pop{pickrand(sobj, wheel)};
