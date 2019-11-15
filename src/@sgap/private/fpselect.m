function e = fpselect(sobj, pop, wheel)
% select element of population member using fitness-proportional roulette wheel

e = pop{pickrand(sobj, wheel)};
